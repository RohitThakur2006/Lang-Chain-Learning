from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.header("Machine Learning Expert")
Chat_prompt=ChatPromptTemplate([
    ("system", "You are helpful {domain} expert"),
    ("human", "Tell me something about the {topic}")
]
)
model=ChatGoogleGenerativeAI(
    model ="gemini-3.1-flash-lite",
    api_key=os.environ.get("API_KEY"),
)

topic=st.selectbox(
    "select which topic you want to do research about",
("Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Self-Supervised Learning", "NLP", "Computer Vision", "Generative AI")
)
if st.button("Search"):
    formatted_prompt=Chat_prompt.invoke({
        "domain": "Machine Learning", 
        "topic": topic
    })
    parser=StrOutputParser()

    response=model.invoke(formatted_prompt)
    final_text=parser.invoke(response)

    st.write(final_text)