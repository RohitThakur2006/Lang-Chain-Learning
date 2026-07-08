from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
import os
from dotenv import load_dotenv
import streamlit as st
st.header("City Experience enhancer")
load_dotenv()
parser=StrOutputParser()

model=ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    api_key=os.environ.get("API_KEY")
)

city_input=st.text_input("Enter your city name here")
if city_input:
    prompt1=PromptTemplate.from_template("You are a local tourist guide and you need to help me find all the best location in the city {city} and answer gracefull and be concise")
    prompt2=PromptTemplate.from_template("You are local city guide and i need you to tell me all about the different dishes in the city {city} and the place where i can find them and be graceful and concise")
    prompt3=PromptTemplate.from_template("You are a city local guide and i need you to create a proper time table for me that i should follow to get the most our of the {city} be graceful and concise in your answers")

    parallel_chain=RunnableParallel(
        chain1= prompt1 | model | parser,
        chain2=prompt2 | model | parser,
        chain3=prompt3 | model | parser,

    )
    result=parallel_chain.invoke({"city": city_input})

    st.subheader("Best places")
    st.write(result["chain1"])
    st.subheader("Best Food")
    st.write(result["chain2"])
    st.subheader("Best timetable")
    st.write(result["chain3"])
    