from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timezone

app = FastAPI()

class Employee(BaseModel):
    id: int
    name: str
    age: int
    department: str
    created_at: datetime


employees = [
    {"id": 1, "name": "John Doe", "age": 30, "department": "HR", "created_at": datetime.now().date()},
    {"id": 2, "name": "Jane Smith", "age": 25, "department": "Finance", "created_at": datetime.now().date()},
    {"id": 3, "name": "Mike Johnson", "age": 35, "department": "IT", "created_at": datetime.now().date()}
]


@app.get("/employees")
def list_employees():
    return employees


@app.get("/employee/{emp_id}")
def get_employee(emp_id:int):
    for emp in employees:
        if emp["id"] == emp_id:
            return emp
    return {"error": "Employee not found"}

@app.post("/employee")
def create_employee(emp: Employee):
    employees.append(emp)
    return {"message": "Employee created successfully"}


@app.delete("/employee/{emp_id}")
def delete_employee(emp_id:int):
    for emp in employees:
        if emp["id"] == emp_id:
            employees.remove(emp)
            return {"message": "Employee deleted successfully"}
    return {"error": "Employee not found"}

