"""
Pydantic data models for structured Resume parsing, ATS scoring, and tailoring.
"""
from typing import List, Optional, Union
from pydantic import BaseModel, Field

class ContactInfo(BaseModel):
    name: str = Field(description="Full name of candidate")
    email: Optional[str] = Field(default="", description="Email address")
    phone: Optional[str] = Field(default="", description="Phone number")
    location: Optional[str] = Field(default="", description="City, State / Country")
    linkedin: Optional[str] = Field(default="", description="LinkedIn URL or handle")
    github: Optional[str] = Field(default="", description="GitHub URL or portfolio link")

class ExperienceItem(BaseModel):
    title: str = Field(description="Job Title")
    company: str = Field(description="Company / Organization Name")
    location: Optional[str] = Field(default="", description="Location")
    dates: str = Field(description="Employment duration (e.g., Jun 2022 - Present)")
    bullets: List[str] = Field(description="High-impact bullet points demonstrating achievements and aligned keywords")

class EducationItem(BaseModel):
    degree: str = Field(description="Degree and field of study")
    institution: str = Field(description="University or Institution")
    dates: Optional[str] = Field(default="", description="Dates attended or graduation year")
    details: Optional[str] = Field(default="", description="GPA, honors, or relevant coursework")

class ProjectItem(BaseModel):
    name: str = Field(description="Project Name")
    technologies: Optional[str] = Field(default="", description="Technologies / Tech stack used")
    link: Optional[str] = Field(default="", description="URL or repo link")
    bullets: List[str] = Field(description="Key contributions and metrics")

class SkillCategory(BaseModel):
    category: str = Field(
        description="Category name (e.g., 'Primary Frontend Expertise', 'AI-Assisted Development', 'Tools & Ecosystem', 'Secondary / Exposure', 'Cloud & Architecture')"
    )
    skills: List[str] = Field(
        description="List of specific skills, tools, or libraries under this category"
    )

class ResumeData(BaseModel):
    contact: ContactInfo
    summary: str = Field(description="Compelling, keyword-targeted professional summary (3-4 sentences)")
    skill_categories: List[SkillCategory] = Field(
        default_factory=list,
        description="Categorized competencies for enhanced ATS readability and executive scanning (e.g., Primary Expertise, AI-Assisted Development, Tools & Ecosystem, Secondary/Exposure)"
    )
    skills: Optional[List[str]] = Field(
        default_factory=list, 
        description="Flat fallback list of skills for backwards compatibility"
    )
    experience: List[ExperienceItem] = Field(description="Work experience items")
    education: List[EducationItem] = Field(description="Education items")
    projects: Optional[List[ProjectItem]] = Field(default_factory=list, description="Notable projects")
    certifications: Optional[List[str]] = Field(default_factory=list, description="Certifications and awards")

class ATSCategoryScore(BaseModel):
    category: str = Field(description="Category name (e.g. Keyword Match, Experience Alignment, Formatting & Readability, Impact & Metrics)")
    score: int = Field(description="Score out of 100")
    feedback: str = Field(description="Detailed feedback on this category")

class ATSAnalysis(BaseModel):
    overall_score: int = Field(description="Overall ATS compatibility score (0-100)")
    category_scores: List[ATSCategoryScore] = Field(description="Detailed scores across categories")
    matching_keywords: List[str] = Field(description="Keywords from JD found in resume")
    missing_keywords: List[str] = Field(description="Critical JD keywords missing from resume")
    strengths: List[str] = Field(description="Key strengths of the tailored resume")
    improvements_made: List[str] = Field(description="Specific tailoring enhancements made")
    critical_advice: List[str] = Field(description="Actionable advice for interviews or applications")

class TailoredResumeResponse(BaseModel):
    resume_data: ResumeData
    ats_analysis: ATSAnalysis
