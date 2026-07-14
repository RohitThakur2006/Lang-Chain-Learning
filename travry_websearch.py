import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    api_key=os.environ.get("API_KEY"),
    temperature=0
)

tool = TavilySearch(
    max_results=5,
    topic="general",
    # include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    # include_domains=None,
    # exclude_domains=None
)

llm_with_tools=llm.bind_tools([tool])


response=llm_with_tools.invoke(
    "Tell me todays latest news from all around the world"
)

print(response.tool_calls)

tool_call=response.tool_calls[0]

result=tool.invoke(tool_call["args"])

text = f"I need you to remove all the /n or other unnecessary thing from this given text and make it best human readable {str(result)}"

# Create a chain that automatically extracts the string
formatting_chain = llm | StrOutputParser()

# Invoke the chain instead of just the LLM
final_response = formatting_chain.invoke(text)

print("\n" + "="*50)
print("🤖 GEMINI'S FORMATTED NEWS SUMMARY:")
print("="*50 + "\n")

# Now final_response is a clean string!
print(final_response)