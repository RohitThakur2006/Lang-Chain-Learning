from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import streamlit as  st

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
if st.button("Search"):
    combinedinput=f"You are a college researcher and now you have to generate 5 point on the college {option} in a aggressive tone" 

    result=model.invoke(combinedinput)

    st.write(result.text)