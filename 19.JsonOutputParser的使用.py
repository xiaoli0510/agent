from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_qwq import ChatQwen

"""
将AIMessage转换为dict,为后续的提示词提供提示词模板

"""
llm = ChatQwen(
    model="qwen-max",
    base_url="https://ws-fybpg29h6nlemy6l.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    max_tokens=3_000,
    timeout=None,
    max_retries=2,
    # other params...
)

first_template = PromptTemplate.from_template("我的邻居姓：{lastname},生了一个{gender}，帮我取一个名字，用json的格式输出答案，key是name,value是你取的名字")

second_template = PromptTemplate.from_template("请用两个词语解释一下这个名字{name}")

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

chain = first_template | llm | json_parser | second_template | llm | str_parser
res = chain.invoke({"lastname": "少", "gender": "女儿"})
print(res, type(res))