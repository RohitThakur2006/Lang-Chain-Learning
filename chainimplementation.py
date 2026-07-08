from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
parser=StrOutputParser()
st.header("Ask any of your queries")
model=ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    api_key=os.environ.get("API_KEY")
)
prompt=ChatPromptTemplate([
    ("system","You have to answer to my queries while disrespecting me"),
    ("user", "My query is about {query}")
])

query=st.text_input("Your query")

combined=prompt.invoke({
    "query":query
})

output=model.invoke(combined)
parsing=parser.invoke(output)
st.write(parsing)