from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

API_URL = "https://api-inference.huggingface.co/models/AliKhaled123/bert-resume-skills-extractor"

class ResumeInput(BaseModel):
    text: str

@app.post("/extract")
def extract_skills(payload: ResumeInput):
    # إرسال النص للموديل بحروف صغيرة
    response = requests.post(API_URL, json={"inputs": payload.text.lower()})

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Hugging Face Server Error")

    results = response.json()
    extracted_skills = set()

    # القائمة السوداء للتنظيف الجذري
    blacklist = {
        'gal', 'august', 'september', 'july', 'cib', 'iti', 'trends', 'enrollment',
        'banking operations', 'commercial international bank', 'information technology institute',
        'financial data work', 'student', 'information technology'
    }

    for entity in results:
        if entity.get('entity_group') == 'SKILL':
            skill = entity['word'].replace("##", "").strip().upper()
            if len(skill) > 2 and skill not in blacklist:
                extracted_skills.add(skill)

    return {"skills": list(sorted(extracted_skills))}
