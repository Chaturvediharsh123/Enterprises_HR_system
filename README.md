# 🤖 AI-Powered HR Assistant

An AI-powered HR Management System built using FastAPI, Streamlit, PostgreSQL, ChromaDB, and Groq LLM. The project combines Employee Management, HR Policy Intelligence, and Retrieval-Augmented Generation (RAG) to provide an intelligent assistant for HR-related queries.

## 🚀 Features

### Employee Management

* Add Employee
* View Employees
* Update Employee Details
* Delete Employee
* Employee Dashboard & Analytics

### HR Policy Assistant (RAG)

* Query HR policy documents using natural language
* ChromaDB Vector Database
* Semantic Search using Embeddings
* Context-Aware Responses using Groq Llama 3.3

### HR Analytics Assistant

* Analyze employee records
* Salary insights
* Employee statistics
* Department and city-based information

## 🛠️ Tech Stack

### Frontend

* Streamlit

### Backend

* FastAPI

### Database

* PostgreSQL

### Vector Database

* ChromaDB

### AI / LLM

* Groq Llama 3.3

### Embeddings

* HuggingFace Embeddings
* all-MiniLM-L6-v2

## 📂 Project Structure

agent_com/

├── Fastapi/

│   ├── main.py

│   └── schema.py

├── Database/

│   ├── db.py

│   ├── session.py

│   └── redis_client.py

├── model/

│   └── employee.py

├── Rag/

│   ├── ingestion.py

│   ├── retrival.py

│   └── llm.py

├── documents/

│   └── POLICY.txt

├── app.py

├── requirements.txt

└── README.md

## ⚙️ Installation

### Clone Repository

git clone <repository-url>

cd agent_com

### Install Dependencies

pip install -r requirements.txt

### Configure Environment Variables

Create a `.env` file:

GROQ_API_KEY=your_groq_api_key

DATABASE_URL=your_database_url

## ▶️ Run Backend

uvicorn Fastapi.main:app --reload

Backend URL:

http://127.0.0.1:8000

## ▶️ Run Frontend

streamlit run app.py

Frontend URL:

http://localhost:8501

## 🧠 RAG Pipeline

1. Upload HR Policy Document
2. Document Loading
3. Text Chunking
4. Embedding Generation
5. ChromaDB Storage
6. Semantic Retrieval
7. Groq LLM Response Generation

## 📊 Future Enhancements

* Multi-document support
* PDF Upload from UI
* Role-Based Access Control
* Attendance Management
* Leave Management System
* Resume Screening Assistant
* Employee Performance Prediction
* HR Chatbot with Memory
* Deployment on AWS/Azure
* LangGraph Multi-Agent Architecture

## 👨‍💻 Author

Harsh Chaturvedi

B.Tech Artificial Intelligence

AI-Powered HR Assistant Project
