"""
FastAPI Backend for Full-Stack Resume Tailorer Agent.
Automatically uses GEMINIAI_API_KEY from .env file.
"""
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.parser import extract_text
from core.agent import tailor_resume, get_api_key
from core.generator import generate_pdf, generate_docx
from core.models import ResumeData, TailoredResumeResponse

app = FastAPI(
    title="Resume Tailorer Agent API",
    description="Intelligent ATS Resume Tailoring Agent powered by Google Gemini",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {
        "status": "ok", 
        "service": "Resume Tailorer Agent API",
        "has_api_key": bool(get_api_key())
    }

@app.post("/api/tailor", response_model=TailoredResumeResponse)
async def api_tailor_resume(
    resume_file: Optional[UploadFile] = File(None),
    jd_file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None),
    jd_text: Optional[str] = Form(None),
    model_name: Optional[str] = Form("gemini-3-flash-preview")
):
    # Resolve Resume text
    final_resume_text = ""
    if resume_file and resume_file.filename:
        content = await resume_file.read()
        final_resume_text = extract_text(content, resume_file.filename)
    elif resume_text and resume_text.strip():
        final_resume_text = resume_text.strip()

    # Resolve JD text
    final_jd_text = ""
    if jd_file and jd_file.filename:
        content = await jd_file.read()
        final_jd_text = extract_text(content, jd_file.filename)
    elif jd_text and jd_text.strip():
        final_jd_text = jd_text.strip()

    if not final_resume_text:
        raise HTTPException(status_code=400, detail="Missing resume! Please upload a PDF/DOCX or provide resume text.")
    if not final_jd_text:
        raise HTTPException(status_code=400, detail="Missing Job Description! Please upload a PDF/DOCX or provide JD text.")

    try:
        result = tailor_resume(
            resume_text=final_resume_text,
            jd_text=final_jd_text,
            model_name=model_name or "gemini-3-flash-preview"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tailoring failed: {str(e)}")

@app.post("/api/download/pdf")
async def download_pdf_endpoint(resume_data: ResumeData):
    try:
        pdf_bytes = generate_pdf(resume_data)
        filename = f"{resume_data.contact.name.replace(' ', '_')}_Tailored_Resume.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@app.post("/api/download/docx")
async def download_docx_endpoint(resume_data: ResumeData):
    try:
        docx_bytes = generate_docx(resume_data)
        filename = f"{resume_data.contact.name.replace(' ', '_')}_Tailored_Resume.docx"
        return Response(
            content=docx_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DOCX generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
