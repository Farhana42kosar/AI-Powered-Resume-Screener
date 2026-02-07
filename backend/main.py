import joblib
import io
import re
from fastapi import FastAPI, UploadFile, File
from PyPDF2 import PdfReader
from processor import get_job_recommendations,calculate_ats_score

app = FastAPI()

# LOAD YOUR MODELS (Ensure these files are in the 'models/' folder)
model = joblib.load("models/LR_model.pkl")
tfidf= joblib.load("models/tfidf_vec.pkl")
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
@app.post("/predict")
async def predict_resume(file: UploadFile = File(...)):
    content = await file.read()
    pdf = PdfReader(io.BytesIO(content))
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    processed_text = clean_text(text)
    # 1. ML Prediction (The broad domain from your trained model)
    vectorized = tfidf.transform([processed_text])
    ml_domain = model.predict(vectorized)[0]
     
    probs = model.predict_proba(vectorized)
    confidence = max(probs[0])
    # 2. Skill Match Logic (The specific roles)
    recommendations = get_job_recommendations(text)
    
    # 3. ATS Score
    top_match_pct = recommendations[0]['match_percentage']
    ats_score = calculate_ats_score(text, top_match_pct)

    return {
       "filename": file.filename,
        "predicted_domain": ml_domain,
        "model_confidence": f"{round(confidence * 100, 2)}%",
        "ats_score": f"{ats_score}%",
        "job_recommendations": recommendations
    }