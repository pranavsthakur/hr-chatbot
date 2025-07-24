from fastapi import FastAPI, HTTPException
from backend.models import ChatRequest, Employee
from typing import List
from backend.search import cached_search, generate_response

app = FastAPI(title="HR Resource Query Chatbot")

@app.get("/")
async def home():
    return {"message": "HR Resource Query Chatbot API is running"}

@app.get("/employees/search", response_model=List[Employee])
async def employee_search(skill: str = None):
    """Search employees by skill"""
    if skill is not None and not skill.strip():
        raise HTTPException(status_code=400, detail="Skill parameter cannot be empty.")

    try:
        query = f"Find employees with {skill}" if skill else "Find employees"
        employees = cached_search(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

    if not employees:
        raise HTTPException(status_code=404, detail="No employees found matching the query.")
    return employees

@app.get("/employees/available", response_model=List[Employee])
async def available_employees():
    """Get only employees who are currently available"""
    try:
        employees = cached_search("available employees")
        if not employees:
            raise HTTPException(status_code=404, detail="No available employees found.")
        return [e for e in employees if e["availability"].lower() == "available"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch available employees: {str(e)}")

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Chat endpoint that returns AI-generated HR response"""
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    try:
        employees = cached_search(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Employee search failed: {str(e)}")

    if not employees:
        return {
            "response": f"No suitable employees found for query: '{request.query}'.",
            "results": []
        }

    try:
        response_text = generate_response(request.query, list(employees))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Response generation failed: {str(e)}")

    return {"response": response_text, "results": list(employees)}
