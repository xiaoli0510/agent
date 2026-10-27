from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore

model = ChatTongyi(
    model="qwen-max",
    base_url="https://ws-fybpg29h6nlemy6l.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料：{context}。"),
    ("user", "用户提问：{input}")
])

# 创建向量存储
vectorstore = InMemoryVectorStore(embedding=DashScopeEmbeddings(model="text-embedding-v4"))
vectorstore.add_texts(
    ["减肥就是要少吃多练", "在减脂期间吃东西很重要要，清淡少油控制卡路里摄入并运动起来", "跑步是很好的运动哦"]
)

input_text = "怎么减肥"

# 检索向量库
result = vectorstore.similarity_search(input_text, 2)

# 参考资料txt
reference_text = "["
for item in result:
    reference_text += item.page_content
reference_text += "]"


def print_prompt(prompt):
    print(type(prompt),prompt.to_string())
    print("=" * 20)
    return prompt


chain = prompt | print_prompt | model | StrOutputParser()

res = chain.invoke({
    "context": reference_text,
    "input": input_text
})
print(res)
