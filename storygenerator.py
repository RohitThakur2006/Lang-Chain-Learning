from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.runnables import RunnableBranch
load_dotenv()
parser=StrOutputParser()

st.header("Story Generator")

model=ChatGoogleGenerativeAI(
    model ="gemini-3.1-flash-lite",
    api_key=os.environ.get("API_KEY"),
)
story_input=st.number_input("Enter your age")

if story_input:
    prompt1=PromptTemplate.from_template("I need you to tell me a horror story for a person of age {age} which will kick me out of my bed in the night")
    prompt2=PromptTemplate.from_template("I need you to tell me a children story for a children of age {age} which will help me sleep in the night")
    chain1=prompt1 | model | parser
    chain2=prompt2 | model | parser
    conditional_chain=RunnableBranch(
        (lambda x: x["age"] > 18, chain1),
        (lambda x: x["age"] < 18, chain2),
        chain1
    )
    with st.spinner("Your story is loading..."):
        result=conditional_chain.invoke({"age": story_input})
        st.write(result)