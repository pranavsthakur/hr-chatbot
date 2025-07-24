import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os
from functools import lru_cache

# Initialize OpenAI client (new API)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load dataset
with open("backend/employees.json", "r") as f:
    employees_data = json.load(f)["employees"]

# Initialize embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Prepare employee documents
employee_texts = [
    f"{emp['name']} with skills {', '.join(emp['skills'])}, "
    f"{emp['experience_years']} years experience, "
    f"projects: {', '.join(emp['projects'])}, availability: {emp['availability']}"
    for emp in employees_data
]

# Encode embeddings
embeddings = model.encode(employee_texts, convert_to_numpy=True)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

@lru_cache(maxsize=50)
def cached_search(query: str, top_k: int = 3):
    """Cached search for faster response"""
    query_vector = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_vector, top_k)
    return tuple(employees_data[i] for i in indices[0])

def generate_response(query: str, employees: list):
    """Generate HR-friendly response using GPT with fallback"""
    if not employees:
        return f"No suitable employees found for query: '{query}'."

    summary = "\n".join([
        f"- {e['name']} ({e['experience_years']} yrs) | Skills: {', '.join(e['skills'])} "
        f"| Projects: {', '.join(e['projects'])} | Availability: {e['availability']}"
        for e in employees
    ])

    prompt = f"""
You are an HR assistant. A user asked: "{query}"
Here are potential employees:
{summary}
Write a friendly and professional HR recommendation message.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert HR assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception:
        # Fallback template response
        return (
            f"Based on your query '{query}', here are the top matches:\n" +
            "\n".join([
                f"- {e['name']} ({e['experience_years']} yrs experience), Skills: {', '.join(e['skills'])}, "
                f"Projects: {', '.join(e['projects'])}, Availability: {e['availability']}"
                for e in employees
            ]) +
            "\nWould you like me to check their availability for a meeting?"
        )
