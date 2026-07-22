from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class AgentState(TypedDict):
    name: str
    age: int
    marks: list[int]
    msg: str

def greetings(state: AgentState) -> dict:  # Changed return type to dict
    name = state["name"]
    greeting_msg = f"Hello dear {name}, hope you are doing well. "
    
    # FIX 1: Return the delta, not the whole state
    return {"msg": greeting_msg}

def output(state: AgentState) -> dict:
    name = state["name"]
    age = state["age"]
    marks = state["marks"]
    
    # FIX 2: Get the current message (the greeting) from the state first
    current_msg = state.get("msg", "")
    
    # Append the new information to the current message
    new_msg = f"{current_msg}Your name is {name}, your age is {age}, and your total marks are {sum(marks)}. Have fun!"
    
    return {"msg": new_msg}

graph = StateGraph(AgentState)

graph.add_node("details", output)
graph.add_node("greeting", greetings)

graph.add_edge(START, "greeting")
graph.add_edge("greeting", "details") 
graph.add_edge("details", END)

app = graph.compile()

initial_state = {
    "name": "Jangey",
    "age": 23,
    "marks": [85, 90, 95],
    "msg": ""
}

result = app.invoke(initial_state)
print(result["msg"])