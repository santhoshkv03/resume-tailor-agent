# AI Resume Tailorer & ATS Optimizer Agent

An autonomous AI agent that ingests candidate resumes and job descriptions (in **PDF** or **Word DOCX** formats), tailors the resume to align with the target role, optimizes keyword density for a high ATS score, and generates clean, professional **PDF** and **Word DOCX** resumes.

This repository provides **both versions** in one workspace:
1. **Option 1: Full-Stack Web Application** (Python FastAPI Backend + React/Vite Modern UI with live preview, score visualization, and PDF/DOCX downloads).
2. **Option 2: Streamlit All-in-One Python Web Application** (Rapid, interactive Python web app).

---

## 🏗️ Architecture & Project Structure

```
resume-tailorer-agent/
├── core/                        # Shared Agent Engine
│   ├── parser.py                # PDF & DOCX text extraction
│   ├── models.py                # Pydantic schemas (ResumeData, ATSAnalysis)
│   ├── agent.py                 # Gemini GenAI agent + intelligent fallback engine
│   └── generator.py             # ATS-compliant PDF (ReportLab) & DOCX (python-docx)
├── fullstack-app/               # Project 1: Full-Stack Web Application
│   ├── backend/
│   │   └── main.py              # FastAPI endpoints (/api/tailor, /api/download/*)
│   └── frontend/                # React + Vite + Lucide + Canvas-Confetti
│       ├── src/App.jsx
│       └── src/index.css
├── streamlit-app/               # Project 2: Streamlit Web Application
│   └── app.py                   # Streamlit interactive UI
├── venv/                        # Python virtual environment
└── README.md
```


---

## ⚡ Quick Start

### 1. Activate Environment & Install Dependencies
```bash
cd /Users/nayanahv/.gemini/antigravity-ide/scratch/resume-tailorer-agent
source venv/bin/activate
```

### 2. Configure Gemini API Key (Optional)
If you have a Gemini API key:
```bash
export GEMINI_API_KEY="your-gemini-api-key"
```
*(Note: If no API key is provided, the agent activates its built-in intelligent heuristic engine so you can test all features offline out-of-the-box).*

---

## 🚀 Running Project 1: Full-Stack App (FastAPI + React)

### Backend (FastAPI on Port 8000)
```bash
./venv/bin/uvicorn main:app --app-dir fullstack-app/backend --host 0.0.0.0 --port 8000 --reload
```

### Frontend (React/Vite on Port 5173)
```bash
cd fullstack-app/frontend
npm run dev -- --host 0.0.0.0 --port 5173
```
👉 Open your browser at: **`http://localhost:5173`**

---

## 🎈 Running Project 2: Streamlit App

```bash
cd /Users/nayanahv/.gemini/antigravity-ide/scratch/resume-tailorer-agent
./venv/bin/streamlit run streamlit-app/app.py --server.port 8501
```
👉 Open your browser at: **`http://localhost:8501`**

---

## 🐳 Running with Docker & Docker Compose

Run the entire full-stack app (FastAPI backend + React frontend + Nginx reverse proxy) in isolated containers:

```bash
# 1. Build and start containers
docker compose up --build -d

# 2. View status
docker compose ps

# 3. View container logs
docker compose logs -f
```

- **Frontend Application**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000` (and `http://localhost:8000/docs` for Swagger UI)
- To stop the services:
  ```bash
  docker compose down
  ```

---

## 📚 Living System Design Documents (SDD)

This repository maintains modular, living specification documents following industry SDD standards:

- 🏛️ **System Architecture & Data Flow:** [docs/spec/system-architecture.md](file:///Users/nayanahv/.gemini/antigravity-ide/scratch/resume-tailorer-agent/docs/spec/system-architecture.md)
- 📋 **Work Breakdown & Tasks:** [docs/spec/tasks.md](file:///Users/nayanahv/.gemini/antigravity-ide/scratch/resume-tailorer-agent/docs/spec/tasks.md)
- ⚙️ **Backend API & Contracts:** [fullstack-app/backend/docs/spec/README.md](file:///Users/nayanahv/.gemini/antigravity-ide/scratch/resume-tailorer-agent/fullstack-app/backend/docs/spec/README.md)
- 🎨 **Frontend UI & Components:** [fullstack-app/frontend/docs/spec/README.md](file:///Users/nayanahv/.gemini/antigravity-ide/scratch/resume-tailorer-agent/fullstack-app/frontend/docs/spec/README.md)
- 🎈 **Streamlit UI Architecture:** [streamlit-app/docs/spec/README.md](file:///Users/nayanahv/.gemini/antigravity-ide/scratch/resume-tailorer-agent/streamlit-app/docs/spec/README.md)

---

## 🎯 ATS Rules & Standards Implemented

1. **Alignment with Target Job Description**:
   - Parses both inputs (PDF/DOCX).
   - Identifies high-value skills, technologies, and methodologies.
   - Weaves them into the summary, skill tags, and experience bullets.
2. **High ATS Score**:
   - Evaluates resume across 4 dimensions: Keyword Match, Experience Alignment, ATS Readability, and Impact/Metrics.
   - Computes missing vs matched keywords.
   - Applies the **Google XYZ formula** (*"Accomplished [X] as measured by [Y] by doing [Z]"*).
3. **Professional & Clean Formatting**:
   - Standard ATS single-column hierarchy.
   - Clean typography (Arial/Helvetica).
   - Direct export to **PDF** and **DOCX**.
