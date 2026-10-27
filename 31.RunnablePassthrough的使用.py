from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore

model = ChatTongyi(
    model="qwen-max",
    base_url="https://ws-fybpg29h6nlemy6l.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model="text-embedding-v4"))
vector_store.add_texts(
    ["减肥就是要少吃多练", "在减脂期间吃东西很重要要，清淡少油控制卡路里摄入并运动起来", "跑步是很好的运动哦"]
)
input_text = "怎么减肥?"

prompt = ChatPromptTemplate.from_messages([
    ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料：{context}。"),
    ("user", "用户提问：{input}")
])

#.as_retriever返回一个Runnable接口的子类实例对象
retriever =vector_store.as_retriever(search_kwargs={"k":2})

# 将list转为str
def format_func(docs:list[Document]):
    if not docs:
        return "无相关参考资料"

    formatted_str = "["
    for doc in docs:
        formatted_str += doc.page_content
    formatted_str += "]"
    return formatted_str


# RunnablePassthrough会自动添加{"input":xx}，所以invoke里面只能写str。retriever.invoke(str)来检索
chain = (
    {"input": RunnablePassthrough(), "context": retriever | format_func} | prompt | model | StrOutputParser()
)

res = chain.invoke(input_text)
print(res)

"""
 retriever
     - 输入：用户的提问  str
     - 输出:向量库的检索结果 list[Document]
 prompt
     - 输入：用户的提问+ 向量库的检索结果 dict
     - 输出：完整的提示词 PromptValue
 综合分析chain的第一个组件应该是prompt而不是retriever,但是前面需要使用RunnablePassthrough
"""
