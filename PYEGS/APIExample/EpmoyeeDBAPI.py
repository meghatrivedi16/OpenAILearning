from fastapi import FastAPI
import DbConnection


app = FastAPI()



@app.get("/employeesDB")
def list_employees():
    return DbConnection.get_employees()

@app.get("/employeeDB/{emp_id}")
def get_employee(emp_id: int):
    return DbConnection.get_employee(emp_id)

@app.post("/employeeDB")
def create_employee(employee: dict):
    return DbConnection.create_employee(employee)

@app.delete("/employeeDB/{emp_id}")
def delete_employee(emp_id: int):
    return DbConnection.delete_employee(emp_id)
