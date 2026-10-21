import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { 
  FileText, Upload, Sparkles, CheckCircle2, AlertCircle, 
  Download, Zap, Briefcase, Award, Check
} from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_URL || '';

export default function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jdFile, setJdFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [jdText, setJdText] = useState('');
  const [modelName, setModelName] = useState('gemini-3-flash-preview');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [tailoredData, setTailoredData] = useState(null);
  const [backendReady, setBackendReady] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/api/health`)
      .then(res => res.json())
      .then(data => {
        if (data.status === 'ok') setBackendReady(true);
      })
      .catch(() => setBackendReady(false));
  }, []);

  // Demo sample loader
  const loadSampleData = () => {
    setResumeText(`John Doe
johndoe@email.com | +1 (555) 019-2834 | San Francisco, CA | linkedin.com/in/johndoe | github.com/johndoe

Summary:
Software developer with 4 years of experience building web applications and backend systems using Python and JavaScript. Passionate about problem-solving, clean code, and working with team members to deliver features.

Skills:
Python, JavaScript, Flask, Django, PostgreSQL, Git, HTML, CSS, REST APIs, Basic Docker.

Experience:
Software Engineer | Acme Technologies | 2021 - Present
- Built features for customer-facing web dashboard.
- Maintained database queries and resolved production bugs.
- Worked with team of 5 engineers in Agile sprints.

Junior Developer | ByteWave Corp | 2019 - 2021
- Created internal scripts to automate data entry.
- Built backend endpoints using Flask.

Education:
BS in Computer Science | San Jose State University | 2019`);

    setJdText(`Role: Senior Full Stack Engineer (AI & Cloud Platforms)
Company: NextGen Systems

We are looking for an exceptional Senior Full Stack Engineer to build our next-generation cloud services and Generative AI workflows.

Key Responsibilities:
- Architect and scale high-performance REST and GraphQL microservices using Python (FastAPI/Django) and modern TypeScript/React.
- Deploy and manage containerized applications using Docker, Kubernetes, and AWS/GCP cloud infrastructure.
- Partner with product managers and AI researchers to implement LLM pipelines and automated agents.
- Drive engineering excellence, automated CI/CD testing, and mentor junior engineers.

Required Qualifications:
- 3+ years experience with Python (FastAPI, Flask or Django) and modern front-end frameworks (React).
- Strong experience with Cloud services (AWS or GCP), Docker, and CI/CD pipelines.
- Solid understanding of database architecture (PostgreSQL, Redis) and distributed systems.
- Familiarity with Generative AI / LLMs, LangChain, or agentic frameworks is a strong plus.`);
  };

  const handleTailor = async () => {
    if (!resumeFile && !resumeText.trim()) {
      setError('Please provide a resume by uploading a file or pasting text.');
      return;
    }
    if (!jdFile && !jdText.trim()) {
      setError('Please provide a Job Description by uploading a file or pasting text.');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    if (resumeFile) formData.append('resume_file', resumeFile);
    if (resumeText.trim()) formData.append('resume_text', resumeText);
    if (jdFile) formData.append('jd_file', jdFile);
    if (jdText.trim()) formData.append('jd_text', jdText);
    formData.append('model_name', modelName);

    try {
      const res = await fetch(`${API_BASE}/api/tailor`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errJson = await res.json().catch(() => ({}));
        throw new Error(errJson.detail || `Server error (${res.status})`);
      }

      const data = await res.json();
      setTailoredData(data);
      confetti({
        particleCount: 80,
        spread: 60,
        origin: { y: 0.6 }
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const downloadFile = async (type) => {
    if (!tailoredData) return;
    try {
      const res = await fetch(`${API_BASE}/api/download/${type}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(tailoredData.resume_data),
      });
      if (!res.ok) throw new Error('Download failed');
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const cleanName = tailoredData.resume_data.contact.name.replace(/\s+/g, '_');
      a.download = `${cleanName}_Tailored_Resume.${type === 'pdf' ? 'pdf' : 'docx'}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      alert(`Error downloading ${type.toUpperCase()}: ${err.message}`);
    }
  };

  const ats = tailoredData?.ats_analysis;
  const resume = tailoredData?.resume_data;

  return (
    <div style={{ minHeight: '100vh', paddingBottom: '4rem' }}>
      {/* Top Navbar */}
      <header className="app-header">
        <div className="header-container">
          <div className="logo-area">
            <div className="logo-icon">
              <Sparkles size={22} color="#ffffff" />
            </div>
            <div>
              <span className="logo-title">ResumeCraft AI</span>
              <span className="logo-badge">ATS Tailorer Agent</span>
            </div>
          </div>
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <button className="btn-outline" onClick={loadSampleData}>
              ⚡ Load Sample Resume & JD
            </button>
          </div>
        </div>
      </header>

      <main className="app-container">
        {/* Hero Section */}
        <div className="hero-banner">
          <h1 className="hero-title">Tailor Your Resume with Gemini AI</h1>
          <p className="hero-subtitle">
            Upload your resume and the target job description. The agent automatically aligns your experience,
            optimizes ATS keywords, and outputs clean, professional PDF and DOCX files.
          </p>
        </div>

        {/* Configuration Bar */}
        <div className="glass-panel config-bar">
          <div className="config-inputs">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ 
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                background: 'rgba(52, 211, 153, 0.15)',
                border: '1px solid rgba(52, 211, 153, 0.3)',
                color: '#6ee7b7',
                padding: '4px 10px',
                borderRadius: '999px',
                fontSize: '0.85rem',
                fontWeight: 600
              }}>
                <Check size={14} /> Gemini API Key Configured (.env)
              </span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontSize: '0.85rem', color: '#94a3b8' }}>Model:</span>
              <select 
                value={modelName}
                onChange={(e) => setModelName(e.target.value)}
                className="text-input"
                style={{ minWidth: '220px' }}
              >
                <option value="gemini-3-flash-preview">gemini-3-flash-preview (Recommended)</option>
                <option value="gemini-3.5-flash">gemini-3.5-flash</option>
                <option value="gemini-flash-latest">gemini-flash-latest</option>
              </select>
            </div>
          </div>
          <button 
            className="btn-primary" 
            onClick={handleTailor}
            disabled={loading}
          >
            {loading ? (
              <>
                <div className="spinner" />
                <span>Tailoring with Gemini AI...</span>
              </>
            ) : (
              <>
                <Zap size={18} />
                <span>Tailor & Score Resume</span>
              </>
            )}
          </button>
        </div>

        {error && (
          <div style={{
            background: 'rgba(239, 68, 68, 0.15)',
            border: '1px solid rgba(239, 68, 68, 0.4)',
            color: '#fca5a5',
            padding: '1rem',
            borderRadius: '10px',
            marginBottom: '1.5rem',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}

        {/* Input Grid: Resume vs JD */}
        <div className="input-grid">
          {/* Resume Box */}
          <div className="glass-panel" style={{ padding: '1.5rem' }}>
            <div className="card-title">
              <FileText size={20} color="#38bdf8" />
              <span>1. Current Resume (PDF, DOCX, or Text)</span>
            </div>
            
            <label className={`upload-dropzone ${resumeFile ? 'active' : ''}`} style={{ display: 'block' }}>
              <input 
                type="file" 
                accept=".pdf,.docx,.doc" 
                style={{ display: 'none' }}
                onChange={(e) => setResumeFile(e.target.files[0] || null)}
              />
              <Upload size={28} color={resumeFile ? "#38bdf8" : "#94a3b8"} style={{ margin: '0 auto 8px auto' }} />
              <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>
                {resumeFile ? resumeFile.name : 'Click to Upload Resume (.pdf or .docx)'}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '4px' }}>
                Automated text extraction from PDF or Word
              </div>
            </label>

            <textarea 
              className="textarea-field"
              placeholder="Or paste your existing resume plain text here..."
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
            />
          </div>

          {/* JD Box */}
          <div className="glass-panel" style={{ padding: '1.5rem' }}>
            <div className="card-title">
              <Briefcase size={20} color="#818cf8" />
              <span>2. Target Job Description (PDF, DOCX, or Text)</span>
            </div>

            <label className={`upload-dropzone ${jdFile ? 'active' : ''}`} style={{ display: 'block' }}>
              <input 
                type="file" 
                accept=".pdf,.docx,.doc" 
                style={{ display: 'none' }}
                onChange={(e) => setJdFile(e.target.files[0] || null)}
              />
              <Upload size={28} color={jdFile ? "#818cf8" : "#94a3b8"} style={{ margin: '0 auto 8px auto' }} />
              <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>
                {jdFile ? jdFile.name : 'Click to Upload Job Description (.pdf or .docx)'}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '4px' }}>
                Key requirements, skills, and qualifications extracted
              </div>
            </label>

            <textarea 
              className="textarea-field"
              placeholder="Or paste the job description here..."
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
            />
          </div>
        </div>

        {/* Tailored Results Dashboard */}
        {tailoredData && (
          <div style={{ marginTop: '3rem' }}>
            {/* ATS Score Banner */}
            <div className="glass-panel score-hero-card">
              <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
                <div className="score-circle">
                  <div className="score-number">{ats.overall_score}</div>
                  <div className="score-label">ATS Score</div>
                </div>
                <div>
                  <h2 style={{ fontSize: '1.6rem', fontWeight: 800, marginBottom: '6px' }}>
                    ATS Match Analysis & Optimization
                  </h2>
                  <p style={{ color: '#94a3b8', fontSize: '0.95rem' }}>
                    Successfully aligned candidate profile with target job requirements. Standard single-column layout ready for recruiter review.
                  </p>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '1rem' }}>
                <button className="btn-primary" onClick={() => downloadFile('pdf')}>
                  <Download size={18} />
                  <span>Download PDF</span>
                </button>
                <button className="btn-outline" onClick={() => downloadFile('docx')}>
                  <Download size={18} />
                  <span>Download DOCX</span>
                </button>
              </div>
            </div>

            {/* Category Scores */}
            <div className="category-grid">
              {ats.category_scores.map((cat, idx) => (
                <div key={idx} className="glass-panel category-card">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#e2e8f0' }}>{cat.category}</span>
                    <span style={{ fontSize: '1rem', fontWeight: 700, color: '#38bdf8' }}>{cat.score}%</span>
                  </div>
                  <div className="progress-bar-bg">
                    <div 
                      className="progress-bar-fill" 
                      style={{ 
                        width: `${cat.score}%`, 
                        background: cat.score >= 85 ? '#34d399' : cat.score >= 70 ? '#38bdf8' : '#f87171' 
                      }} 
                    />
                  </div>
                  <p style={{ fontSize: '0.8rem', color: '#94a3b8', lineHeight: 1.4 }}>{cat.feedback}</p>
                </div>
              ))}
            </div>

            {/* Keywords Matched & Missing */}
            <div className="input-grid" style={{ marginBottom: '2rem' }}>
              <div className="glass-panel" style={{ padding: '1.25rem' }}>
                <div style={{ fontWeight: 700, marginBottom: '8px', color: '#6ee7b7', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <CheckCircle2 size={16} /> Matched & Integrated Keywords ({ats.matching_keywords.length})
                </div>
                <div>
                  {ats.matching_keywords.map((kw, i) => (
                    <span key={i} className="tag-chip tag-match">{kw}</span>
                  ))}
                </div>
              </div>

              <div className="glass-panel" style={{ padding: '1.25rem' }}>
                <div style={{ fontWeight: 700, marginBottom: '8px', color: '#fca5a5', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <AlertCircle size={16} /> Missing High-Priority Keywords ({ats.missing_keywords.length})
                </div>
                <div>
                  {ats.missing_keywords.length > 0 ? (
                    ats.missing_keywords.map((kw, i) => (
                      <span key={i} className="tag-chip tag-missing">{kw}</span>
                    ))
                  ) : (
                    <span style={{ fontSize: '0.85rem', color: '#94a3b8' }}>All core JD keywords present!</span>
                  )}
                </div>
              </div>
            </div>

            {/* Enhancements Made & Advice */}
            <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '2.5rem' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                <div>
                  <h4 style={{ color: '#38bdf8', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <Sparkles size={16} /> Key Agent Enhancements Made
                  </h4>
                  <ul style={{ paddingLeft: '1.2rem', fontSize: '0.88rem', color: '#cbd5e1', lineHeight: '1.6' }}>
                    {ats.improvements_made.map((item, idx) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 style={{ color: '#fbbf24', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <Award size={16} /> Interview & Application Strategy
                  </h4>
                  <ul style={{ paddingLeft: '1.2rem', fontSize: '0.88rem', color: '#cbd5e1', lineHeight: '1.6' }}>
                    {ats.critical_advice.map((item, idx) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            {/* Document Live Preview */}
            <div style={{ marginBottom: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3 style={{ fontSize: '1.4rem', fontWeight: 800 }}>📄 Tailored Resume Document Preview</h3>
              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <button className="btn-primary" onClick={() => downloadFile('pdf')}>
                  Download PDF
                </button>
                <button className="btn-outline" onClick={() => downloadFile('docx')}>
                  Download DOCX
                </button>
              </div>
            </div>

            <div className="resume-sheet">
              <h1 className="resume-name">{resume.contact.name}</h1>
              <div className="resume-contact-bar">
                {[resume.contact.email, resume.contact.phone, resume.contact.location, resume.contact.linkedin, resume.contact.github]
                  .filter(Boolean)
                  .join('  •  ')}
              </div>

              {resume.summary && (
                <div>
                  <div className="resume-section-title">Professional Summary</div>
                  <p className="resume-summary-text">{resume.summary}</p>
                </div>
              )}

              {/* Categorized Skills */}
              {(resume.skill_categories && resume.skill_categories.length > 0) ? (
                <div>
                  <div className="resume-section-title">Core Competencies & Technical Skills</div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                    {resume.skill_categories.map((catItem, idx) => (
                      <div key={idx} style={{ fontSize: '0.88rem', color: '#334155', lineHeight: '1.45' }}>
                        <strong style={{ color: '#0f172a' }}>{catItem.category}:</strong>{' '}
                        <span>{catItem.skills.join(', ')}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (resume.skills && resume.skills.length > 0) && (
                <div>
                  <div className="resume-section-title">Core Competencies & Technical Skills</div>
                  <div className="resume-skills-text">{resume.skills.join(' • ')}</div>
                </div>
              )}

              {resume.experience && resume.experience.length > 0 && (
                <div>
                  <div className="resume-section-title">Professional Experience</div>
                  {resume.experience.map((exp, idx) => (
                    <div key={idx} style={{ marginBottom: '1rem' }}>
                      <div className="exp-header-row">
                        <div>
                          <strong>{exp.title}</strong> | <em>{exp.company}</em>
                        </div>
                        <div style={{ color: '#0284c7', fontWeight: 600, fontSize: '0.85rem' }}>
                          {exp.dates} {exp.location ? `(${exp.location})` : ''}
                        </div>
                      </div>
                      <ul className="exp-bullets">
                        {exp.bullets.map((b, bIdx) => (
                          <li key={bIdx}>{b}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              )}

              {resume.projects && resume.projects.length > 0 && (
                <div>
                  <div className="resume-section-title">Key Projects</div>
                  {resume.projects.map((proj, idx) => (
                    <div key={idx} style={{ marginBottom: '0.75rem' }}>
                      <div className="exp-header-row">
                        <div>
                          <strong>{proj.name}</strong> {proj.technologies && <em>({proj.technologies})</em>}
                        </div>
                        <div style={{ color: '#64748b', fontSize: '0.85rem' }}>{proj.link}</div>
                      </div>
                      <ul className="exp-bullets">
                        {proj.bullets.map((b, bIdx) => (
                          <li key={bIdx}>{b}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              )}

              {resume.education && resume.education.length > 0 && (
                <div>
                  <div className="resume-section-title">Education</div>
                  {resume.education.map((edu, idx) => (
                    <div key={idx} style={{ marginBottom: '0.5rem' }}>
                      <div className="exp-header-row">
                        <div>
                          <strong>{edu.degree}</strong>, {edu.institution}
                        </div>
                        <div style={{ color: '#0284c7', fontWeight: 600, fontSize: '0.85rem' }}>{edu.dates}</div>
                      </div>
                      {edu.details && <div style={{ fontSize: '0.82rem', color: '#64748b' }}>{edu.details}</div>}
                    </div>
                  ))}
                </div>
              )}

              {resume.certifications && resume.certifications.length > 0 && (
                <div>
                  <div className="resume-section-title">Certifications & Honors</div>
                  <ul className="exp-bullets">
                    {resume.certifications.map((c, idx) => (
                      <li key={idx}>{c}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
