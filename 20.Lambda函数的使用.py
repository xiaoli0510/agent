from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_qwq import ChatQwen

"""
用RunnableLambda包一层，或者之间传函数(__or__会把不是Runnable类的转换为Runnable)

"""
llm = ChatQwen(
    model="qwen3-max",
    base_url="https://ws-fybpg29h6nlemy6l.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    max_tokens=3_000,
    timeout=None,
    max_retries=2,
    # other params...
)

first_template = PromptTemplate.from_template("我的邻居姓：{lastname},生了一个{gender}，帮我取一个名字，只回答名字即可")

str_parser = StrOutputParser()
my_func = RunnableLambda(lambda ai_msg:{"name": ai_msg.content})

second_template = PromptTemplate.from_template(
    "帮我在{name}后面，添加一个妈妈:VV"
)

chain = first_template | llm | (lambda ai_msg:{"name": ai_msg.content}) | second_template | llm
res = chain.invoke({"lastname": "少", "gender": "儿子"})
print(res.content, type(res.content))

chain2 =chain| str_parser
res2 = chain2.invoke({"lastname": "王", "gender": "儿子"})
print(res2, type(res2))