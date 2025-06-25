from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# IBM Watsonx Credentials
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_ID = os.getenv("MODEL_ID")
PROJECT_ID = os.getenv("PROJECT_ID")

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize IBM Model
try:
    creds = Credentials(url=BASE_URL, api_key=API_KEY)
    model = ModelInference(
        model_id=MODEL_ID,
        credentials=creds,
        project_id=PROJECT_ID
    )
    params = {"decoding_method": "greedy", "max_new_tokens": 300, "min_new_tokens": 10}

except Exception as e:
    print(f"Error initializing model: {e}")
    model = None

# Utility to safely parse model responses
def parse_response(response):
    print(f"Raw Response: {response}")
    if isinstance(response, str):
        return response
    elif isinstance(response, list):
        return response[0]["generated_text"]
    elif isinstance(response, dict) and "results" in response:
        return response["results"][0]["generated_text"]
    else:
        return "Unexpected response format."

# 1. Chat Assistant
@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get("user_input")

        if not user_input:
            return {"response": "Please provide a query."}

        response = model.generate_text(prompt=user_input, params=params)
        reply = parse_response(response)
        return {"response": reply}

    except Exception as e:
        print(f"Backend Error: {e}")
        return {"response": f"Error: {str(e)}"}

# 2. Disease Predictor
@app.post("/predict_disease")
async def predict_disease(request: Request):
    try:
        data = await request.json()
        symptoms = data.get("symptoms")

        if not symptoms:
            return {"prediction": "Please provide symptoms to predict the disease."}

        prompt = f"Based on these symptoms: {symptoms}, what is the most likely disease?"
        response = model.generate_text(prompt=prompt, params=params)
        prediction = parse_response(response)
        return {"prediction": prediction}

    except Exception as e:
        print(f"Backend Error: {e}")
        return {"prediction": f"Error: {str(e)}"}

# 3. Treatment Plan Generator
@app.post("/generate_treatment")
async def generate_treatment(request: Request):
    try:
        data = await request.json()
        disease = data.get("disease")

        if not disease:
            return {"treatment_plan": "Please provide a disease name."}

        prompt = f"Suggest a detailed treatment plan for {disease}."
        response = model.generate_text(prompt=prompt, params=params)
        treatment_plan = parse_response(response)
        return {"treatment_plan": treatment_plan}

    except Exception as e:
        print(f"Backend Error: {e}")
        return {"treatment_plan": f"Error: {str(e)}"}

# 4. Health Analytics
@app.post("/health_analytics")
async def health_analytics(request: Request):
    try:
        data = await request.json()
        health_data = data.get("health_data")

        if not health_data:
            return {"analytics": "Please provide health data for analysis."}

        prompt = f"Analyze the following patient health data and provide detailed insights: {health_data}"
        response = model.generate_text(prompt=prompt, params=params)
        analytics = parse_response(response)
        return {"analytics": analytics}

    except Exception as e:
        print(f"Backend Error: {e}")
        return {"analytics": f"Error: {str(e)}"}


        

    
        


    
