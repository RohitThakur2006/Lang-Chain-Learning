from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    msg: str

def greeting_node(state: AgentState) -> AgentState:
    state['msg']="Hello, World!!"
    return state

graph=StateGraph(AgentState)
graph.add_node("helloworld", greeting_node)
graph.set_entry_point("helloworld")
graph.set_finish_point("helloworld")
app=graph.compile()

result=app.invoke({"msg": ""})
print(result)

