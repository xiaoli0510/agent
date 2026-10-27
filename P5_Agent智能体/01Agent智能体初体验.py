from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool

"""
  工具让LM有了感知外部世界并影响现实的能力
"""


@tool(description="查询天气")
def get_weather() -> str:
    return "晴天"
agent = create_agent(
    model=ChatTongyi(model="qwen-max"),
    tools=[get_weather],
    system_prompt="你是一个聊天助手，回答用户问题"
)

res = agent.invoke(
    {
        "messages":[
            {"role": "user", "content": "明天深圳的天气如何?"}
        ]
    }
)

"""
 res是字典，通过[xx]来获取属性，字典只存取内容，是js中的json
 对象是类实例化的，是带有说明书的数据，自带方法和属性，通过.来获取方法和属性
"""
for msg in res["messages"]:
    print(type(msg).__name__,msg.content)
