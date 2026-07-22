from typing import TypedDict 
from langgraph.graph import StateGraph, START, END

# 1. Update State to include the new parameters and an intermediate result
class AgentState(TypedDict):
    num1: float
    num2: float
    num3: float
    operation1: str  # For "+" or "-"
    operation2: str  # For "*" or "/"
    intermediate_num: float
    final_num: float

# --- FIRST STAGE NODES (+ / -) ---
def adder(state: AgentState) -> AgentState:
    state["intermediate_num"] = state["num1"] + state["num2"]
    return state

def subtractor(state: AgentState) -> AgentState:
    state["intermediate_num"] = state["num1"] - state["num2"]
    return state

# --- SECOND STAGE NODES (* / /) ---
def multiplier(state: AgentState) -> AgentState:
    state["final_num"] = state["intermediate_num"] * state["num3"]
    return state

def divider(state: AgentState) -> AgentState:
    state["final_num"] = state["intermediate_num"] / state["num3"]
    return state

# --- CONDITIONAL NODES ---
def conditional_node_1(state: AgentState) -> AgentState:
    return state

def conditional_node_2(state: AgentState) -> AgentState:
    return state

# --- DECIDER FUNCTIONS ---
def decider_function_1(state: AgentState) -> str:
    if state["operation1"] == "+":
        return "addition_edge"
    if state["operation1"] == "-": 
        return "subtraction_edge"

def decider_function_2(state: AgentState) -> str:
    if state["operation2"] == "*":
        return "multiplication_edge"
    if state["operation2"] == "/": 
        return "division_edge"

# Initialize Graph
graph = StateGraph(AgentState)

# Add All Nodes
graph.add_node("add_node", adder)
graph.add_node("subtract_node", subtractor)
graph.add_node("multiply_node", multiplier)
graph.add_node("divide_node", divider)
graph.add_node("conditional_node_1", conditional_node_1)
graph.add_node("conditional_node_2", conditional_node_2)

# --- DEFINE THE GRAPH FLOW ---

# 1. Entry point goes to the first conditional node
graph.add_edge(START, "conditional_node_1")

# 2. First condition routes to Add or Subtract
graph.add_conditional_edges(
    "conditional_node_1",
    decider_function_1,
    {
        "addition_edge": "add_node",
        "subtraction_edge": "subtract_node",
    },
)

# 3. Both Add and Subtract nodes flow into the second conditional node
graph.add_edge("add_node", "conditional_node_2")
graph.add_edge("subtract_node", "conditional_node_2")

# 4. Second condition routes to Multiply or Divide
graph.add_conditional_edges(
    "conditional_node_2",
    decider_function_2,
    {
        "multiplication_edge": "multiply_node",
        "division_edge": "divide_node",
    },
)

# 5. Multiply and Divide route to the end of the graph
graph.add_edge("multiply_node", END)
graph.add_edge("divide_node", END)

# Compile
app = graph.compile()

# Invoke
result = app.invoke({
    "num1": 10, 
    "num2": 5, 
    "num3": 2, 
    "operation1": "+", 
    "operation2": "*",
    "intermediate_num": 0,
    "final_num": 0
})

print(result)