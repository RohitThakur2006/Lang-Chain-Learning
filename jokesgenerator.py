from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import streamlit as st

st.header("Joke Generator")
input1=st.text_input("You are a joke yourself")
load_dotenv()
model1=ChatGoogleGenerativeAI(
model="gemini-3.1-flash-lite",
api_key=os.environ.get("API_KEY"),
)
model2=ChatGoogleGenerativeAI(
model="gemini-2.5-flash-lite",
api_key=os.environ.get("API_KEY"),
)

if input1:
    parser=StrOutputParser()
    system_prompt="Tell me the best joke which you have heard on {query}"
    prompt1=PromptTemplate.from_template(system_prompt)
    system_prompt1=" tell me a better joke than this {joke}"
    prompt2=PromptTemplate.from_template(system_prompt1)
    system_prompt2="You are a jokes critique and i need you to tell me the differences between {joke1} and {joke2} in a aggressive way"
    prompt3=PromptTemplate.from_template(system_prompt2)
    
    chain1=prompt1 | model2 | parser
    chain2=prompt2 | model1 | parser
    chain3=prompt3 | model1 | parser


    joke1_text=chain1.invoke({"query": input1})
    joke2_text=chain2.invoke({"joke": joke1_text})
    joke3_text=chain3.invoke({
        "joke1": joke1_text,
        "joke2": joke2_text,
    })

    st.subheader("joke 1")
    st.write(joke1_text)
    st.subheader("joke 2")
    st.write(joke2_text)
    st.subheader("analysis: ")
    st.write(joke3_text)