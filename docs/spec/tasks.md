# Project Task Breakdown & Implementation Roadmap
**Document Type:** Living Work Breakdown Structure (WBS) & Sprint Board  
**Status:** Living Document  
**Version:** 1.0.0  

---

## 📋 Task Matrix

| Task ID | Component | Module | Task Description | Priority | Status |
|---|---|---|---|---|---|
| **CORE-101** | Core Engine | `parser.py` | Implement PDF in-memory extraction via `pypdf` | P0 | ✅ Done |
| **CORE-102** | Core Engine | `parser.py` | Implement DOCX text and table extraction via `python-docx` | P0 | ✅ Done |
| **CORE-103** | Core Engine | `models.py` | Define `ResumeData`, `ATSAnalysis`, and category Pydantic models | P0 | ✅ Done |
| **CORE-104** | Core Engine | `agent.py` | Integrate Gemini SDK with system prompt & structured JSON schema | P0 | ✅ Done |
| **CORE-105** | Core Engine | `agent.py` | Build intelligent heuristic offline engine with XYZ rule fallback | P1 | ✅ Done |
| **CORE-106** | Core Engine | `generator.py` | Implement single-column ATS PDF generator using ReportLab | P0 | ✅ Done |
| **CORE-107** | Core Engine | `generator.py` | Implement clean Word DOCX generator with section dividing lines | P0 | ✅ Done |
| **CORE-108** | Core Engine | `agent.py` | Implement automatic `.env` key loader (`GEMINIAI_API_KEY`) | P0 | ✅ Done |
| **CORE-109** | Core Engine | `agent.py` | Update default LLM model to `gemini-3-flash-preview` | P0 | ✅ Done |
| **BE-201** | Backend | `main.py` | Initialize FastAPI app with CORS middleware | P0 | ✅ Done |
| **BE-202** | Backend | `main.py` | Implement multipart `/api/tailor` endpoint | P0 | ✅ Done |
| **BE-203** | Backend | `main.py` | Implement `/api/download/pdf` endpoint | P0 | ✅ Done |
| **BE-204** | Backend | `main.py` | Implement `/api/download/docx` endpoint | P0 | ✅ Done |
| **BE-205** | Backend | `main.py` | Implement `/api/health` with environment check | P1 | ✅ Done |
| **BE-206** | Backend | `test_suite` | Implement automated unit & integration tests for API endpoints | P2 | ⏳ Backlog |
| **FE-301** | Frontend | `vite/react` | Scaffold Vite React SPA with dark mode design system | P0 | ✅ Done |
| **FE-302** | Frontend | `App.jsx` | Implement dual file upload dropzones (PDF/DOCX) + text fallback | P0 | ✅ Done |
| **FE-303** | Frontend | `App.jsx` | Implement ATS scoring dashboard with circular gauge & progress bars | P0 | ✅ Done |
| **FE-304** | Frontend | `App.jsx` | Implement matched vs missing keyword badge visualization | P0 | ✅ Done |
| **FE-305** | Frontend | `App.jsx` | Implement live rendered resume sheet with standard ATS typography | P0 | ✅ Done |
| **FE-306** | Frontend | `App.jsx` | Implement one-click PDF & DOCX binary download handlers | P0 | ✅ Done |
| **FE-307** | Frontend | `App.jsx` | Remove user-facing key prompts and display internal .env badge | P0 | ✅ Done |
| **FE-308** | Frontend | `App.jsx` | Add in-browser editable fields for tailored resume tuning before download | P2 | ⏳ Next |
| **ST-401** | Streamlit | `app.py` | Build dual-column upload interface for resume and JD | P0 | ✅ Done |
| **ST-402** | Streamlit | `app.py` | Implement metric cards, progress bars, and keyword badges | P0 | ✅ Done |
| **ST-403** | Streamlit | `app.py` | Implement PDF & DOCX download buttons | P0 | ✅ Done |
| **ST-404** | Streamlit | `app.py` | Remove API key text input and auto-detect `.env` key | P0 | ✅ Done |
| **DOC-501** | Docs/SDD | `specs` | Create modular living SDD documentation across core, backend, frontend | P0 | ✅ Done |

---

## 🔄 Lifecycle of Living Tasks

1. **Active**: Currently assigned and being written or refactored.
2. **Review/Validation**: Code is built, unit-tested, and verified locally.
3. **Done**: Documented and verified in running application.
4. **Backlog/Next**: Future enhancements planned for successive iterations.
