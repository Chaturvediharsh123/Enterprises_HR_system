from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import JSONLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import Docx2txtLoader
import os

file = "documents/POLICY.txt"

print("Current Directory:", os.getcwd())
print("File Exists:", os.path.exists(file))
print("File:", file)

if file.endswith(".pdf"):
    loader=PyPDFLoader(file)
    doc=loader.load()
    
elif file.endswith(".docx"):
    loader = Docx2txtLoader(file)
    doc = loader.load()
    
elif file.endswith(".txt"):
    loader = TextLoader(file)
    doc = loader.load()
    
elif file.endswith(".csv"):
    loader=CSVLoader(file)
    doc=loader.load()
    
elif file.endswith(".json"):
    loader = JSONLoader(
    file_path=file,
    jq_schema="."
)
    doc=loader.load()
    
else:
    raise ValueError(
        "Only PDF, CSV and JSON are supported"
    )

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
docs=text_splitter.split_documents(doc)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./chroma_db"
)


print(
    f"Stored {len(docs)} chunks"
)