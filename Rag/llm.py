# from langchain_ollama import ChatOllama

# def llm():
#     llm=ChatOllama(
#     model="phi3:mini",
# )

# result=llm.invoke("tell me a short story")

# print(result.content)
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)