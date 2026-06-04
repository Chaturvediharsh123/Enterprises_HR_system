from sqlalchemy import Column,Integer,String,Float
from Database.db import Base,engine

class Employee(Base):

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    salary = Column(Float)
    city = Column(String)
    gender = Column(String)

Base.metadata.create_all(bind=engine)