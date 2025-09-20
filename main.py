from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
import random
import time
import asyncio
from datetime import datetime

app = FastAPI(title="Agent Testing API", decription="Simple API for learning agent development")

# Sample data for realistic testing
EMPLOYEES_DATA = {
    1: {"id": 1, "name": "Alice Johnson", "department": "Engineering", "phone": "+1-555-0101", "manager_id": 5, "salary": 95000, "hire_date": "2022-01-15"},
    2: {"id": 2, "name": "Bob Smith", "department": "Marketing", "phone": "+1-555-0102", "manager_id": 6, "salary": 78000, "hire_date": "2021-03-22"},
    3: {"id": 3, "name": "Carol Davis", "department": "HR", "phone": None, "manager_id": 7, "salary": 65000, "hire_date": "2020-11-08"},
    4: {"id": 4, "name": "David Wilson", "department": "Engineering", "phone": "+1-555-0104", "manager_id": 5, "salary": 88000, "hire_date": "2023-02-14"},
    5: {"id": 5, "name": "Eva Martinez", "department": "Engineering", "phone": "+1-555-0105", "manager_id": None, "salary": 120000, "hire_date": "2019-05-30"},
    6: {"id": 6, "name": "Frank Chen", "department": "Marketing", "phone": "+1-555-0106", "manager_id": None, "salary": 105000, "hire_date": "2018-09-12"},
    7: {"id": 7, "name": "Grace Lee", "department": "HR", "phone": "+1-555-0107", "manager_id": None, "salary": 95000, "hire_date": "2020-01-20"},
    8: {"id": 8, "name": "Henry Brown", "department": "Finance", "phone": "+1-555-0108", "manager_id": 9, "salary": 72000, "hire_date": "2022-07-03"},
    9: {"id": 9, "name": "Iris Taylor", "department": "Finance", "phone": "+1-555-0109", "manager_id": None, "salary": 110000, "hire_date": "2017-12-01"},
    10: {"id": 10, "name": "Jack Anderson", "department": "Engineering", "phone": None, "manager_id": 5, "salary": 82000, "hire_date": "2023-04-18"}
}

DEPARTMENTS_DATA = {
    "Engineering": {"name": "Engineering", "head": "Eva Martinez", "budget": 5000000, "location": "Building A, Floor 3"},
    "Marketing": {"name": "Marketing", "head": "Frank Chen", "budget": 2000000, "location": "Building B, Floor 2"},
    "HR": {"name": "Human Resources", "head": "Grace Lee", "budget": 800000, "location": "Building A, Floor 1"},
    "Finance": {"name": "Finance", "head": "Iris Taylor", "budget": 1500000, "location": "Building C, Floor 1"}
}

PROJECTS_DATA = {
    1: {"id": 1, "name": "Mobile App Redesign", "department": "Engineering", "status": "active", "budget": 150000, "start_date": "2023-06-01"},
    2: {"id": 2, "name": "Brand Campaign 2024", "department": "Marketing", "status": "planning", "budget": 300000, "start_date": "2024-01-15"},
    3: {"id": 3, "name": "Employee Wellness Program", "department": "HR", "status": "completed", "budget": 75000, "start_date": "2023-03-01"},
    4: {"id": 4, "name": "Financial System Upgrade", "department": "Finance", "status": "active", "budget": 200000, "start_date": "2023-08-15"},
    5: {"id": 5, "name": "API Integration", "department": "Engineering", "status": "delayed", "budget": 120000, "start_date": "2023-09-01"}
}

# Sim functions for real world scnearios

# simulating real world API latency
async def simulate_latency():
    delay = random.uniform(0.1, 2.0)
    await asyncio.sleep(delay)
    return delay 

# simulate error message 10% of the time
async def simulate_error(error_rate = 0.1):
    rand = random.random()

    # 40% are 500s
    if rand < error_rate * 0.4:
        raise HTTPException(status_code=500, detail = "Internal server error - database timeout")
    elif rand < error_rate * 0.7:
        raise HTTPException(status_code=503, detail ="Services temporarily unavailable")
    elif rand < error_rate:
        raise HTTPException(status_code=504, detial = "Gateway timeout")


# model class for request/response validation
class EmployeeResponse(BaseModel):
    id: int
    name: str
    department: str
    phone: Optional[str] = None
    manager_id: Optional[int] = None
    hire_date: str


class EmployeeWithSalary(EmployeeResponse):
    salary: int

class DepartmentResponse(BaseModel):
    name: str
    head: str
    budget: int
    location: str


class ProjectResponse(BaseModel):
    id:int
    name: str
    departments: str
    status: str
    budget: int
    start_date: str


# root endpoints contains API information 
@app.get("/")
async def read_root():
    return {
        "message": "Agent Learning API",
        "description": "Simple API for learning agent development",
        "endpoints": {
            "employees": "/employees",
            "departments": "/departments", 
            "projects": "/projects",
            "search": "/search"
        }
    }


@app.get("/employees", response_model=List[EmployeeResponse])
async def get_employees(
    departmen: Optional[str] = Query(None, description="Filter by department"),
    limit: int = Query(10, ge=1, le=100, description="Limit number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    
    # list of employees with filtering

    await simulate_latency()

    # error hits 5% of the time
    simulate_error(0.05)

    employees = list(EMPLOYEES_DATA.values())

    # apply filter if it exists
    if department:
        employees = [emp for emp in employees if emp["department"] == department]

    start = offset
    end = offset + limit
    paginated_employees = employees[start:end]

    return paginated_employees


#get employee by id
@app.get("/employees{employee_id}", response_model = EmployeeResponse)
async def get_employee(employee_id: int):
    
    await simulate_latency()
    simulate_error(0.1) # 10% error rate

    if employee_id not in EMPLOYEES_DATA:
        raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found")

    return EMPLOYEES_DATA[employee_id]


# get employee salary
@app.get("/employees/{employee_id}/salary", response_model=EmployeeWithSalary)
async def get_employee_salary(employee_id: int):
    await simulate_latency()
    simulate_error(0.08)
    
    if employee_id not in EMPLOYEES_DATA:
        raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found")
    
    employee = EMPLOYEES_DATA[employee_id].copy()
    return employee


@app.get("/departments", response_model=List[DepartmentResponse])
async def get_departments():

    await simulate_latency()
    simulate_error(0.03) # 3% error rate

    return list(DEPARTMENTS_DATA.values())


# get specific department info by name
@app.get("/departments/{department_name}", response_model=DepartmentResponse)
async def get_department(department_name: str):
    await simulate_latency()
    simulate_error(0.05)
    
    if department_name not in DEPARTMENTS_DATA:
        raise HTTPException(status_code=404, detail=f"Department '{department_name}' not found")
    
    return DEPARTMENTS_DATA[department_name]


@app.get("/projects", response_model=List[ProjectResponse])
async def get_projects(
    status: Optional[str] = Query(None, description="Filter by status"),
    department: Optional[str] = Query(None, description="Filter by department")
):
    """Get projects with optional filtering"""
    await simulate_latency()
    simulate_error(0.07)
    
    projects = list(PROJECTS_DATA.values())
    
    if status:
        projects = [proj for proj in projects if proj["status"] == status]
    
    if department:
        projects = [proj for proj in projects if proj["department"] == department]
    
    return projects

@app.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int):
    """Get specific project by ID"""
    await simulate_latency()
    simulate_error(0.08)
    
    if project_id not in PROJECTS_DATA:
        raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
    
    return PROJECTS_DATA[project_id]

@app.get("/search")
async def search(
    q: str = Query(..., description="Search query"),
    type: str = Query("all", description="Search type: all, employees, departments, projects")
):
    """Universal search across all data types"""
    await simulate_latency()
    simulate_error(0.06)
    
    query_lower = q.lower()
    results = {"employees": [], "departments": [], "projects": []}
    
    # Search employees
    if type in ["all", "employees"]:
        for emp in EMPLOYEES_DATA.values():
            if (query_lower in emp["name"].lower() or 
                query_lower in emp["department"].lower()):
                results["employees"].append(emp)
    
    # Search departments
    if type in ["all", "departments"]:
        for dept in DEPARTMENTS_DATA.values():
            if (query_lower in dept["name"].lower() or 
                query_lower in dept["head"].lower() or
                query_lower in dept["location"].lower()):
                results["departments"].append(dept)
    
    # Search projects
    if type in ["all", "projects"]:
        for proj in PROJECTS_DATA.values():
            if (query_lower in proj["name"].lower() or 
                query_lower in proj["department"].lower() or
                query_lower in proj["status"].lower()):
                results["projects"].append(proj)
    
    return {
        "query": q,
        "type": type,
        "results": results,
        "total_results": sum(len(v) for v in results.values())
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    # Simulate occasional health check failures
    if random.random() < 0.02:  # 2% failure rate
        raise HTTPException(status_code=503, detail="Health check failed")
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    await simulate_latency()
    
    return {
        "total_employees": len(EMPLOYEES_DATA),
        "total_departments": len(DEPARTMENTS_DATA),
        "total_projects": len(PROJECTS_DATA),
        "employees_by_department": {
            dept: len([emp for emp in EMPLOYEES_DATA.values() if emp["department"] == dept])
            for dept in DEPARTMENTS_DATA.keys()
        },
        "projects_by_status": {
            status: len([proj for proj in PROJECTS_DATA.values() if proj["status"] == status])
            for status in set(proj["status"] for proj in PROJECTS_DATA.values())
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)