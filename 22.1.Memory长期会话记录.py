from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_qwq import ChatQwen

"""
其实新的InMemorySaver管的是agent的状态
LLM不支持短期记忆，需要自己写代码来实现
agent才支持短期记忆，但是InMemorySaver只适合测试开发，本质是将对话历史存到RAM内存中。进程退出数据没了，无法多进程/多服务器共享
生产环境使用基于PostgreSQL数据库的检查点类

"""

def print_prompt(prompt):
    print("="*20, prompt, "="*20)
    return prompt

llm = ChatQwen(
    model="qwen-max",
    base_url="https://ws-fybpg29h6nlemy6l.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    max_tokens=3_000,
    timeout=None,
    max_retries=2,
    # other params...
)

agent = create_agent(
    model=llm,
    tools=[],
    checkpointer=InMemorySaver(),
)




thread_config = {"configurable": {"thread_id": "1"}}
response = agent.invoke(
    {"messages": [
        {"role": "system", "content": "you are a boy,and you like pithy answer."},
        {"role": "user", "content": "Hi! I like rice"}
    ]},
    thread_config,
)["messages"][-1].content

print(response)  # "Hi Bob! Nice to see you here. How are you doing?"

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what do you like?"}]},
    thread_config,
)["messages"][-1].content

print(response)  # "You are Bob!"