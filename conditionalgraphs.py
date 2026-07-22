from typing import TypedDict 
from langgraph.graph import StateGraph, START, END

# 1. Define the variables our state will hold
class AgentState(TypedDict):
    num1: int
    num2: int
    operation: str
    final_num: int

def adder(state: AgentState) -> AgentState:
    state["final_num"] = state["num1"] + state["num2"]
    return state

def subtractor(state: AgentState) -> AgentState:
    state["final_num"] = state["num1"] - state["num2"]
    # 2. Added missing return statement
    return state

def conditional_node(state: AgentState) -> AgentState:
    return state

def decider_function(state: AgentState) -> str:
    # 3. Fixed spelling and mapped exactly to the dictionary below
    if state["operation"] == "+":
        return "addition_edge"
    if state["operation"] == "-": 
        return "subtraction_edge"

# Initialize Graph
graph = StateGraph(AgentState)

# Add Nodes
graph.add_node("add_node", adder)
graph.add_node("subtract_node", subtractor)
graph.add_node("conditional_node", conditional_node)

# Set Entry Point
graph.add_edge(START, "conditional_node")

# Map Conditional Edges
graph.add_conditional_edges(
    "conditional_node",
    decider_function,
    {
        "addition_edge": "add_node",
        "subtraction_edge": "subtract_node",
    },
)

# 4. Route terminal nodes to the END of the graph
graph.add_edge("add_node", END)
graph.add_edge("subtract_node", END)

# Compile
app = graph.compile()

# Invoke
result = app.invoke({"num1": 10, "num2": 5, "operation": "+", "final_num": 0})
print(result)