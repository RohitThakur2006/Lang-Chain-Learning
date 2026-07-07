from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import streamlit as  st
from langchain_core.output_parsers import StrOutputParser 
from langchain_core.prompts import PromptTemplate
st.header("Dynamic Colleger Researcher")
load_dotenv()
model=ChatGoogleGenerativeAI(
    model ="gemini-3.1-flash-lite",
    api_key=os.environ.get("API_KEY"),
)
option=st.selectbox(
    "Select which university you want to know mroe about",
    ("LPU", "CU", "Amity", "CIPLA")
)

parser=StrOutputParser()
if st.button("Search"):
    prompt_template=PromptTemplate(
        template="You are a college researcher and now you have to generate 5 point on the college {option} in a aggressive tone",
        input_variables= ["option"],
    )
    # combinedinput=f"You are a college researcher and now you have to generate 5 point on the college {option} in a aggressive tone" 
    formatted_prompt=prompt_template.format(option=option)
    response=model.invoke(formatted_prompt)

    result=parser.invoke(response)
    st.write(result)