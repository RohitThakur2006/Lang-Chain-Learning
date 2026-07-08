from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import streamlit as st

st.header("Joke Generator")
input1=st.text_input("You are a joke yourself")
load_dotenv()
if input1:
    parser=StrOutputParser()
    model=ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        api_key=os.environ.get("API_KEY"),
    )
    system_prompt="Tell me the best joke which you have heard on {query}"
    prompt=PromptTemplate.from_template(system_prompt)
    chain=prompt | model | parser
    output=chain.invoke({"query": input1})
    st.write(output)