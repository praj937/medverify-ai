from fastapi import FastAPI, File, UploadFile
import random

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend running"}

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    # Simple document classification
    if "prescription" in text.lower():
        doc_type = "Prescription"
    else:
        doc_type = "Medical Document"

    # Simple compliance check
    if "overdose" in text.lower() or "wrong dosage" in text.lower():
        compliance = "Non-Compliant"
    else:
        compliance = "Compliant"

    # Fake detection (random for now)
    score = random.uniform(0, 1)

    return {
        "document_type": doc_type,
        "compliance": compliance,
        "fake_probability": score
    }

@app.post("/chat/")
async def chat(query: str):
    if "compliance" in query.lower():
        return {"response": "Document checked using basic STG rules."}
    elif "fake" in query.lower():
        return {"response": "Forgery detection uses anomaly scoring."}
    return {"response": "Ask about compliance or fake detection."}