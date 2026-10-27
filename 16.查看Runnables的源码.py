from langchain_core.prompts import PromptTemplate
from langchain_qwq import ChatQwen

llm = ChatQwen(
    model="qwen-max",
    max_tokens=3_000,
    timeout=None,
    max_retries=2,
    # other params...
)

prompt = PromptTemplate.from_template("你是谁")

chain = prompt | llm | prompt | llm

print(type(chain))