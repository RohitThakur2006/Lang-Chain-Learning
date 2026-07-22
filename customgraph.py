from langgraph.graph import StateGraph
from typing import TypedDict

class FirstClass(TypedDict):
    name: str

def printgreeting(state: FirstClass) -> FirstClass:
    state["name"]="Hey How are you doing"
    return state

graph=StateGraph(FirstClass)
graph.add_node("hey", printgreeting)
graph.set_entry_point("hey")
graph.set_finish_point("hey")
app=graph.compile()


result=app.invoke({"name": ""})
print(result)