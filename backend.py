from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
MODEL_ID = os.getenv("MODEL_ID")
WATSONX_URL = os.getenv("WATSONX_URL")

class ChatRequest(BaseModel):
    user_input: str

class SymptomRequest(BaseModel):
    symptoms: list

def get_token():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"apikey={API_KEY}&grant_type=urn:ibm:params:oauth:grant-type:apikey"
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def granite_response(prompt):
    token = get_token()
    if not token:
        return "Error: Authentication failed."

    url = f"{WATSONX_URL}/ml/v1/text/chat?version=2023-05-29"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    body = {
        "messages": [
            {"role": "system", "content": "You are a helpful, cautious AI health assistant named HealthAI."},
            {"role": "user", "content": prompt}
        ],
        "project_id": PROJECT_ID,
        "model_id": MODEL_ID,
        "max_tokens": 2000,
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()['results'][0]['generated_text']
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.post("/chat")
def chat(request: ChatRequest):
    reply = granite_response(request.user_input)
    return {"response": reply}

@app.post("/predict-disease")
def predict_disease(request: SymptomRequest):
    symptoms = ", ".join(request.symptoms)
    prompt = f"Based on the symptoms: {symptoms}, what is the most likely disease?"
    reply = granite_response(prompt)
    return {"predicted_disease": reply}

@app.post("/generate-treatment")
def generate_treatment(request: ChatRequest):
    prompt = f"Provide a detailed treatment plan for {request.user_input}."
    reply = granite_response(prompt)
    return {"treatment_plan": reply}

@app.post("/health-analytics")
def health_analytics(request: ChatRequest):
    prompt = f"Analyze the following patient health data and provide insights:\n{request.user_input}"
    reply = granite_response(prompt)
    return {"analytics": reply}
