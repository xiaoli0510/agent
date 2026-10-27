from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool
"""
ReAct模式
思考->行动->观察->思考的循环

思考：分析需求，考虑下一步
行动：工具调用获取信息
观察：分析获取的信息
"""


@tool(description="获取体重，返回值是整数，单位千克")
def get_weight() -> int:
    return 90

@tool(description="获取身高，返回值是整数，单位厘米")
def get_height() -> int:
    return 172
agent = create_agent(
    model=ChatTongyi(model="qwen-max"),
    system_prompt="""你是严格按照ReAct框架的智能体，必须按照「思考-行动-观察-再思考」的流程解决问题，
    且**每轮仅能思考并调用一个工具**，禁止单次调用多个工具。
    并告知我你的思考过程，工具的调用原因，按思考、行动、观察三个结构告知我""",
    tools=[get_weight, get_height],

)

for chunk in agent.stream(
        {"messages":[
            {"role": "user", "content": "计算我的BMI"}
        ]},
       stream_mode="values"
):
    latest_message = chunk["messages"][-1]
    if latest_message.content:
        print(type(latest_message).__name__, latest_message.content.strip())

    try:
        if latest_message.tool_calls:
            print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")
    except AttributeError:
        pass
