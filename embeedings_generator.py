import os
from dotenv import load_dotenv
# FIX 1: Corrected the spelling of Embeddings here
from langchain_google_genai import GoogleGenerativeAIEmbeddings 
from langchain_chroma import Chroma
from langchain_core.documents import Document

load_dotenv()

doc1 = Document(
    page_content="Albert Einstein was a theoretical physicist known for developing the theory of relativity, one of the two pillars of modern physics.",
    metadata={"field": "Physics", "country": "Germany"}
)

doc2 = Document(
    page_content="Mahatma Gandhi was a leader of India’s non-violent independence movement against British rule and is celebrated for his philosophy of peaceful resistance.",
    metadata={"field": "Politics", "country": "India"}
)

doc3 = Document(
    page_content="Marie Curie was a pioneering scientist who conducted groundbreaking research on radioactivity and was the first woman to win a Nobel Prize.",
    metadata={"field": "Chemistry", "country": "Poland"}
)

doc4 = Document(
    page_content="Leonardo da Vinci was a Renaissance artist and inventor, best known for masterpieces like the Mona Lisa and The Last Supper.",
    metadata={"field": "Art", "country": "Italy"}
)

doc5 = Document(
    page_content="Martin Luther King Jr. was an American civil rights leader who advocated for equality through non-violent civil disobedience.",
    metadata={"field": "Civil Rights", "country": "USA"}
)

docs = [doc1, doc2, doc3, doc4, doc5]
doc_ids = ["id1", "id2", "id3", "id4", "id5"]

vector_store = Chroma(
    # FIX 2: Corrected "gemini-embeedings-2-preview" to "gemini-embedding-2-preview"
    embedding_function=GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview"), 
    persist_directory='my_file_db', 
    collection_name='sample' 
)

# --- 3. Add Documents ---
print("Adding documents to Chroma using Gemini Embeddings...")
vector_store.add_documents(documents=docs, ids=doc_ids)

# --- 4. View Documents ---
print("\n--- Getting Documents ---")
all_docs = vector_store.get(include=['embeddings', 'documents', 'metadatas'])
print(f"Total documents in store: {len(all_docs['documents'])}")

# --- 5. Search Documents ---
print("\n--- Similarity Search ---")
results = vector_store.similarity_search(
    query='Who among these are a physicist',
    k=2 
)
for res in results:
    print(f"- {res.page_content}")

# --- 6. Search with Similarity Score ---
print("\n--- Similarity Search with Score ---")
results_with_score = vector_store.similarity_search_with_score(
    query='Who among these are a physicist',
    k=2
)
for res, score in results_with_score:
    print(f"- {res.page_content} (Score: {score:.4f})")

# --- 7. Metadata Filtering ---
print("\n--- Search with Metadata Filter ---")
filtered_results = vector_store.similarity_search_with_score(
    query="leader",
    filter={'country': 'India'} 
)
for res, score in filtered_results:
    print(f"- {res.page_content} (Score: {score:.4f})")

# --- 8. Updating a Document ---
print("\n--- Updating Document ---")
updated_doc1 = Document(
    page_content="Albert Einstein revolutionized modern physics with his contributions to quantum mechanics and the theory of general relativity. Beyond science, he was a passionate advocate for civil rights and a vocal critic of authoritarianism.",
    metadata={"field": "Physics", "country": "Germany", "notable_for": "Relativity & Humanitarianism"}
)
vector_store.update_document(document_id="id1", document=updated_doc1)
print("Document 'id1' updated successfully.")

# --- 9. Deleting a Document ---
print("\n--- Deleting Document ---")
vector_store.delete(ids=['id5'])
print("Document 'id5' deleted successfully.")