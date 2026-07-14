import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    api_key=os.environ.get("API_KEY"),
    temperature=0
)



@tool
def add_nums(num1: int, num2: int):
    """This function return the sum of two given numbers"""
    return num1+num2

llm_with_tools=llm.bind_tools([add_nums])


response=llm_with_tools.invoke(
    "give me the sum of 4 and 9"
)

print(response.tool_calls)

tool_call=response.tool_calls[0]

result=add_nums.invoke(tool_call["args"])

print(result)