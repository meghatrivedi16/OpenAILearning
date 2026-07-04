import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv() 

url: str = os.environ.get("SUPABASE_URL")

key: str = os.environ.get("SUPABASE_SECRET_KEY")

supabase: Client = create_client(url, key)


# insert
#supabase.table("Employee").insert({"name": "Jane Smith", "age": 25, "department": "Finance"}).execute()
#supabase.table("Employee").insert({"name": "Mike Shield", "age": 35, "department": "Production"}).execute()
#supabase.table("Employee").insert({"name": "Robert Johnson", "age": 30, "department": "Picker"}).execute()

# read
#response = supabase.table("Employee").select("*").execute()
#print(response.data)

def get_employees():
    response = supabase.table("Employee").select("*").execute()
    return response.data

def get_employee(emp_id:int):
    response = supabase.table("Employee").select("*").eq("id", emp_id).execute()
    return response.data

def create_employee(employee: dict):
    response = supabase.table("Employee").insert(employee).execute()
    return response.data

def delete_employee(emp_id: int):
    response = supabase.table("Employee").delete().eq("id", emp_id).execute()
    return response.data