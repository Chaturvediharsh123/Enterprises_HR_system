from fastapi import FastAPI
from Fastapi.schema import empl,emplcreate,emplupdate,chatRequest
from Rag.llm import llm 
from Rag.retrival import retrival
from Database.redis_client import redis
from fastapi import Depends
from sqlalchemy.orm import Session
from Database.session import get_db
from model.employee import Employee


app=FastAPI()

@app.get("/")
async def home():
    return{
"message":"fast api is working "
}


#for rag 

@app.post("/chat")
async def chat(request:chatRequest):
    
    cached_answer = await redis.get(
        request.question
    )

    if cached_answer:
        return {
            "answer": cached_answer,
            "source": "cache"
        }

    docs = retrival(
        request.question
    )
    context="\n\n".join(
        doc.page_content
        for doc in docs
    )
    prompt = f"""
    You are a RAG assistant.

    

    Context:
    {context}

    Question:
    {request.question}

    Answer:
    """
    response=llm.invoke(prompt)
    
    await redis.set(
    request.question,
    response.content,
    ex=3600
)
    
    return{
    "answer":response.content
}
    



@app.post("/employee")
def create_employee(
    employee: emplcreate,
    db: Session = Depends(get_db)
):

    emp = Employee(
        name=employee.name,
        age=employee.age,
        salary=employee.salary,
        city=employee.city,
        gender=employee.gender
    )

    db.add(emp)
    db.commit()
    db.refresh(emp)

    return emp


##get all
@app.get("/employee")
def get_employees(
    db: Session = Depends(get_db)
):

    return db.query(Employee).all()



@app.get("/employee/{id}")
def get_employee(
    id: int,
    db: Session = Depends(get_db)
):

    emp = db.query(Employee).filter(
        Employee.id == id
    ).first()

    return emp



@app.put("/employee/{id}")
def update_employee(
    id: int,
    data: emplupdate,
    db: Session = Depends(get_db)
):

    emp = db.query(Employee).filter(
        Employee.id == id
    ).first()

    if not emp:
        return {"message": "Employee Not Found"}

    if data.name is not None:
        emp.name = data.name

    if data.age is not None:
        emp.age = data.age

    if data.salary is not None:
        emp.salary = data.salary

    if data.city is not None:
        emp.city = data.city

    if data.gender is not None:
        emp.gender = data.gender

    db.commit()
    db.refresh(emp)

    return emp




@app.delete("/employee/{id}")
def delete_employee(
    id: int,
    db: Session = Depends(get_db)
):

    emp = db.query(Employee).filter(
        Employee.id == id
    ).first()

    if not emp:
        return {"message": "Employee Not Found"}

    db.delete(emp)
    db.commit()

    return {"message": "Deleted Successfully"}




@app.post("/employee-chat")
async def employee_chat(
    request: chatRequest,
    db: Session = Depends(get_db)
):

    employees = db.query(Employee).all()

    if not employees:
        return {
            "answer": "No employees found in database"
        }

    context = "\n".join(
        [
            f"""
            Name: {emp.name}
            Age: {emp.age}
            Salary: {emp.salary}
            City: {emp.city}
            Gender: {emp.gender}
            """
            for emp in employees
        ]
    )

    prompt = f"""
    You are an employee database assistant.

    Answer ONLY using the employee data below.

    Employee Data:
    {context}

    Question:
    {request.question}

    Answer:
    """

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }