import os
import wikipedia
from dotenv import load_dotenv

# ---------------------------------------------------------
# 1. MODERN LANGCHAIN IMPORTS (No Deprecated Retrievers)
# ---------------------------------------------------------
from langchain_community.document_loaders import WikipediaLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.documents import Document

# Load environment variables
load_dotenv()

# FIX THE WIKIPEDIA BLOCK
wikipedia.set_user_agent("MyGenAIProject/1.0 (your.email@example.com)")

print("Step 1: Fetching articles from Wikipedia...")
loader = WikipediaLoader(query="China–Pakistan relations", load_max_docs=5)
raw_docs = loader.load()
print(f"Loaded {len(raw_docs)} documents from Wikipedia.")

print("\nStep 2: Initializing Gemini Models...")
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
# Using the active 2026 production model
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)

print("\nStep 3: Creating Vector Store...")
vector_store = InMemoryVectorStore.from_documents(raw_docs, embeddings)

print("\nStep 4: Setting up Retriever Strategy...")
base_retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# ======================================================================
# CHOOSE YOUR STRATEGY (Keep one active, comment out the rest)
# ======================================================================

# --- OPTION 1: MMR (Maximal Marginal Relevance) ---
# retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 3, "fetch_k": 10})


# --- OPTION 2: LCEL Multi-Query (CURRENTLY ACTIVE) ---
# mq_prompt = PromptTemplate.from_template(
#     "Generate 3 different versions of the following question to help search a database.\n"
#     "Provide only the questions separated by newlines.\n"
#     "Question: {question}"
# )
# mq_chain = mq_prompt | llm | StrOutputParser() | (lambda x: x.strip().split("\n"))

# def multi_query_search(question: str):
#     queries = mq_chain.invoke({"question": question})
#     all_docs = []
#     for q in queries:
#         if q: all_docs.extend(base_retriever.invoke(q))
        
#     unique_docs = {doc.page_content: doc for doc in all_docs}
#     return list(unique_docs.values())

# retriever = RunnableLambda(multi_query_search)


# --- OPTION 3: LCEL Contextual Compression ---
cc_prompt = PromptTemplate.from_template(
    "Extract only the relevant information from the Context that answers the Question.\n"
    "If there is no relevant information, reply strictly with NO_RELEVANT_INFO.\n"
    "Question: {question}\nContext: {context}"
)
extractor_chain = cc_prompt | llm | StrOutputParser()

def compress_search(question: str):
    docs = base_retriever.invoke(question)
    compressed_docs = []
    for doc in docs:
        compressed_text = extractor_chain.invoke({
            "question": question, "context": doc.page_content
        })
        if "NO_RELEVANT_INFO" not in compressed_text:
            compressed_docs.append(Document(page_content=compressed_text, metadata=doc.metadata))
    return compressed_docs

retriever = RunnableLambda(compress_search)

# ======================================================================

print("\nStep 5: Performing Semantic Search (Gemini is rewriting your query)...")
query = "geopolitical history and alignment between Beijing and Islamabad against India"
matched_docs = retriever.invoke(query)

for i, doc in enumerate(matched_docs):
    print(f"\n--- Result {i+1} ---")
    print(f"Source Page: {doc.metadata.get('title', 'Unknown')}")
    print(f"Content Snippet:\n{doc.page_content[:500]}...")