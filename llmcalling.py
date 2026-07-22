from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# 1. Define the State
# This dictates what data is passed between nodes
class GraphState(TypedDict):
    input_text: str
    output_text: str

# 2. Define the Nodes
def start_node(state: GraphState):
    """Starting Node: Logs or prepares the incoming request."""
    print("-> [Start Node] Received input:", state.get("input_text"))
    # We just return the state as-is to pass it to the next node
    return state 

def llm_node(state: GraphState):
    """You can call an gemini llm using this node."""
    print("-> [LLM Node] Calling Gemini...")
    
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
    
    # Invoke the LLM with the input text
    response = llm.invoke(state["input_text"])
    
    # Return the new output_text to update the state
    return {"output_text": response.content}

def end_node(state: GraphState):
    """Ending Node: Formats or finalizes the output."""
    print("-> [End Node] Finalizing...")
    
    # Let's add a simple prefix to show this node did some work
    formatted_output = f"✨ Gemini Says: {state.get('output_text')}"
    
    return {"output_text": formatted_output}

# 3. Build the Graph
builder = StateGraph(GraphState)

# Register the three nodes
builder.add_node("start", start_node)
builder.add_node("llm", llm_node)
builder.add_node("end", end_node)

# 4. Define the Edges (The Flow)
builder.add_edge(START, "start")
builder.add_edge("start", "llm")
builder.add_edge("llm", "end")
builder.add_edge("end", END)

# 5. Compile the Graph
graph = builder.compile()

# --- Run the Graph ---
if __name__ == "__main__":
    # Ensure the API key is set before running
    if not os.environ.get("GOOGLE_API_KEY"):
        print("⚠️ Warning: GOOGLE_API_KEY environment variable not set.")
    
    # Provide the initial state
    initial_state = {"input_text": "Write a one-sentence joke about a robot."}
    
    # Invoke the graph
    result = graph.invoke(initial_state)
    
    print("\n--- FINAL GRAPH OUTPUT ---")
    print(result["output_text"])