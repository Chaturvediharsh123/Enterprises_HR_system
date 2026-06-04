from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import Chroma

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
    collection_name="rag_collection"
)

# question = input(
#     "Ask a question: "
# )

def retrival(question):
    return vector_store.similarity_search(
    question,
    k=3)

# print("\nRetrieved Chunks:\n")

# for i, doc in enumerate(results, start=1):
#     print(f"\nChunk {i}")
#     print("-" * 50)
#     print(doc.page_content)

