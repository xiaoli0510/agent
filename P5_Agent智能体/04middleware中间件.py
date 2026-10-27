from langchain.agents import AgentState
from langchain.agents.middleware import before_agent
from langgraph.runtime import Runtime


@before_agent
def log_before_agent(state: AgentState, runtime:Runtime) -> None:
    print(f"[before_agent] agent启用，并附带{len(state['messages'])}消息")
