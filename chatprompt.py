from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

Chat_prompt=ChatPromptTemplate([
    ("system", "You are helpful {domain} expert"),
    ("human", "Tell me something about the {topic}")
]
)
model=ChatGoogleGenerativeAI(
    model ="gemini-3.1-flash-lite",
    api_key=os.environ.get("API_KEY"),
)
formatted_prompt=Chat_prompt.invoke({
    "domain": "astronomy", 
    "topic": "black holes"
})
parser=StrOutputParser()

response=model.invoke(formatted_prompt)
final_text=parser.invoke(response)

print(final_text)