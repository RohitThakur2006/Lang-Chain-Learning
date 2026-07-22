import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

# ... rest of your imports below ...
from dotenv import load_dotenv
from langchain.tools import tool
# ...



# 1. Load env variables after all imports
load_dotenv()

# 2. Fixed model name to a valid current model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite", 
    api_key=os.environ.get("API_KEY"),
    temperature=0
)

@tool
def add_nums(num1: int, num2: int):
    """This function return the sum of two given numbers"""
    return num1 + num2

@tool
def temp(str2: str):
    """This function returns the current temperature of jalandhar"""
    return 36

tools = [add_nums, temp]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# 3. Fixed typo: Agent_Executor -> AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

response = agent_executor.invoke({
    "input": "what is your name"
})

outputsaved=response["output"]
print(outputsaved[0]["text"])