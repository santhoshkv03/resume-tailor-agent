# Backend System Design Document (SDD)
**Component:** Full-Stack Backend API (`fullstack-app/backend`)  
**Living Spec Location:** `fullstack-app/backend/docs/spec/README.md`  
**Status:** Living Spec / Active  
**Version:** 1.0.0  

---

## 1. Overview & Responsibilities

The backend server is built using **FastAPI** (Python 3.9+) and serves as the API gateway between the presentation layer (React SPA) and the core AI agent logic. It handles:
- Multipart file uploads for Resumes and Job Descriptions.
- Text stream extraction (delegated to `core.parser`).
- Orchestrating Gemini model requests with structured schema enforcement.
- Streaming generated PDF and DOCX binary responses.

---

## 2. API Contract Specification

### `GET /api/health`
Checks server availability and environment configuration.

- **Response `200 OK`**:
```json
{
  "status": "ok",
  "service": "Resume Tailorer Agent API",
  "has_api_key": true
}
```

---

### `POST /api/tailor`
Main agent tailoring and ATS scoring endpoint.

- **Content-Type:** `multipart/form-data`
- **Request Parameters:**
  | Field | Type | Required | Description |
  |---|---|---|---|
  | `resume_file` | Binary File | Optional | Resume in `.pdf` or `.docx` format |
  | `resume_text` | String | Optional | Plain text of candidate resume |
  | `jd_file` | Binary File | Optional | Job Description in `.pdf` or `.docx` format |
  | `jd_text` | String | Optional | Plain text of Job Description |
  | `model_name` | String | Optional | Gemini model identifier (default: `gemini-3-flash-preview`) |

*(Validation Rule: At least one of `resume_file` or `resume_text` MUST be provided; and at least one of `jd_file` or `jd_text` MUST be provided).*

- **Response `200 OK` Schema (`TailoredResumeResponse`):**
```json
{
  "resume_data": {
    "contact": {
      "name": "string",
      "email": "string",
      "phone": "string",
      "location": "string",
      "linkedin": "string",
      "github": "string"
    },
    "summary": "string",
    "skills": ["string"],
    "experience": [
      {
        "title": "string",
        "company": "string",
        "location": "string",
        "dates": "string",
        "bullets": ["string"]
      }
    ],
    "education": [
      {
        "degree": "string",
        "institution": "string",
        "dates": "string",
        "details": "string"
      }
    ],
    "projects": [
      {
        "name": "string",
        "technologies": "string",
        "link": "string",
        "bullets": ["string"]
      }
    ],
    "certifications": ["string"]
  },
  "ats_analysis": {
    "overall_score": 92,
    "category_scores": [
      {
        "category": "Keyword Match & Density",
        "score": 95,
        "feedback": "string"
      }
    ],
    "matching_keywords": ["string"],
    "missing_keywords": ["string"],
    "strengths": ["string"],
    "improvements_made": ["string"],
    "critical_advice": ["string"]
  }
}
```

---

### `POST /api/download/pdf`
Generates and returns an ATS-compliant PDF file.

- **Content-Type:** `application/json`
- **Body:** `ResumeData` object.
- **Response `200 OK`**:
  - `Content-Type`: `application/pdf`
  - `Content-Disposition`: `attachment; filename="{Candidate_Name}_Tailored_Resume.pdf"`

---

### `POST /api/download/docx`
Generates and returns an ATS-compliant Word document.

- **Content-Type:** `application/json`
- **Body:** `ResumeData` object.
- **Response `200 OK`**:
  - `Content-Type`: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
  - `Content-Disposition`: `attachment; filename="{Candidate_Name}_Tailored_Resume.docx"`

---

## 3. Error Handling Matrix

| HTTP Status | Trigger Condition | Response Body |
|---|---|---|
| `400 Bad Request` | Neither resume file nor text provided | `{"detail": "Missing resume! Please upload a PDF/DOCX or provide resume text."}` |
| `400 Bad Request` | Neither JD file nor text provided | `{"detail": "Missing Job Description! Please upload a PDF/DOCX or provide JD text."}` |
| `500 Server Error` | Unhandled exception during generation or parsing | `{"detail": "Tailoring failed: <error_message>"}` |

---

## 4. Configuration & Environment Variables

- `GEMINIAI_API_KEY`: Primary API key loaded from root `.env`.
- `GEMINI_API_KEY`: Alternate API key fallback.
- Server runs on `http://0.0.0.0:8000` managed via Uvicorn.
