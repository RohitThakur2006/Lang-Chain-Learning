import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st

st.header("College Resarch Assistant")
load_dotenv()

model= ChatGoogleGenerativeAI(
    model ="gemini-3.1-flash-lite",
    api_key=os.environ.get("API_KEY"),
)

print("User_prompt")
User=st.text_input("Enter your query: ")
if st.button("Research"):
    result=model.invoke(User)
    st.write(result.text)