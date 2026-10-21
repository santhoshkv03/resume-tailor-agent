"""
Generator module to convert structured ResumeData into:
1. ATS-optimized, beautifully styled PDF (via ReportLab)
2. Clean, professional Microsoft Word document (via python-docx)

Ensures exact visual and structural parity with the web preview:
- Accurate page printable width matching (6.8-7.0 inches)
- Standardized tab stops for right-aligned dates & locations
- Zero accidental empty paragraphs
- Professional border divider line for section headings
- Beautiful categorized competencies with bold prefixes
- Consistent, tight, executive line spacing and bullet indentations
"""
import io
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from .models import ResumeData

def generate_docx(resume: ResumeData) -> bytes:
    """
    Generate professional, ATS-optimized Microsoft Word .docx file.
    Uses native right-aligned tab stops (not fragile tables) to perfectly match 
    the web preview's exp-header-row layout and prevent unwanted line wraps or borders.
    """
    doc = Document()
    
    # Standard 0.65 inch margins
    page_width_in = 8.5
    margin_left_in = 0.65
    margin_right_in = 0.65
    content_width_in = page_width_in - (margin_left_in + margin_right_in) # 7.2 inches
    
    for section in doc.sections:
        section.top_margin = Inches(0.65)
        section.bottom_margin = Inches(0.65)
        section.left_margin = Inches(margin_left_in)
        section.right_margin = Inches(margin_right_in)
        section.page_width = Inches(page_width_in)
        section.page_height = Inches(11.0)

    primary_color = RGBColor(15, 23, 42)      # #0F172A (Deep Slate)
    accent_color = RGBColor(2, 132, 199)      # #0284C7 (Electric Teal / Blue)
    text_color = RGBColor(51, 65, 85)         # #334155 (Charcoal body)
    light_text = RGBColor(100, 116, 139)      # #64748B (Muted meta)

    # 1. Header - Candidate Name
    name_p = doc.add_paragraph()
    name_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    name_p.paragraph_format.space_before = Pt(0)
    name_p.paragraph_format.space_after = Pt(2)
    name_run = name_p.add_run(resume.contact.name)
    name_run.font.name = "Arial"
    name_run.font.size = Pt(22)
    name_run.font.bold = True
    name_run.font.color.rgb = primary_color

    # 2. Contact Information Bar
    contact_parts = []
    if resume.contact.email:
        contact_parts.append(resume.contact.email)
    if resume.contact.phone:
        contact_parts.append(resume.contact.phone)
    if resume.contact.location:
        contact_parts.append(resume.contact.location)
    if resume.contact.linkedin:
        contact_parts.append(resume.contact.linkedin)
    if resume.contact.github:
        contact_parts.append(resume.contact.github)

    if contact_parts:
        contact_p = doc.add_paragraph()
        contact_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        contact_p.paragraph_format.space_before = Pt(0)
        contact_p.paragraph_format.space_after = Pt(12)
        c_run = contact_p.add_run("  •  ".join(contact_parts))
        c_run.font.name = "Arial"
        c_run.font.size = Pt(9.5)
        c_run.font.color.rgb = light_text

    def add_section_heading(title: str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(11)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(title.upper())
        run.font.name = "Arial"
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = accent_color
        
        # Add thin, clean bottom border line matching web preview
        pBdr = OxmlElement('w:pBdr')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '6')
        bottom.set(qn('w:space'), '1')
        bottom.set(qn('w:color'), 'E2E8F0')
        pBdr.append(bottom)
        p._p.get_or_add_pPr().append(pBdr)

    # Helper to add a 2-column header row using standard Word right tab
    def add_meta_header_row(left_title: str, left_subtitle: str, right_dates: str, right_loc: str = ""):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.tab_stops.add_tab_stop(Inches(content_width_in), WD_TAB_ALIGNMENT.RIGHT)

        # Left Part: Title | Company
        r_title = p.add_run(left_title)
        r_title.font.name = "Arial"
        r_title.font.size = Pt(10)
        r_title.font.bold = True
        r_title.font.color.rgb = primary_color

        if left_subtitle:
            r_sep = p.add_run(" | ")
            r_sep.font.name = "Arial"
            r_sep.font.size = Pt(10)
            r_sep.font.color.rgb = light_text

            r_sub = p.add_run(left_subtitle)
            r_sub.font.name = "Arial"
            r_sub.font.size = Pt(9.5)
            r_sub.font.italic = True
            r_sub.font.color.rgb = text_color

        # Right Part: Tab to right margin
        p.add_run("\t")

        right_text = right_dates
        if right_loc:
            right_text += f" ({right_loc})"

        r_right = p.add_run(right_text)
        r_right.font.name = "Arial"
        r_right.font.size = Pt(9)
        r_right.font.bold = True
        r_right.font.color.rgb = accent_color

    # 3. Professional Summary
    if resume.summary:
        add_section_heading("Professional Summary")
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(resume.summary)
        run.font.name = "Arial"
        run.font.size = Pt(9.5)
        run.font.color.rgb = text_color

    # 4. Core Competencies & Skills
    has_cats = bool(resume.skill_categories)
    has_flat = bool(resume.skills)
    
    if has_cats or has_flat:
        add_section_heading("Core Competencies & Technical Skills")
        if has_cats:
            for cat_item in resume.skill_categories:
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(2.5)
                p.paragraph_format.line_spacing = 1.15
                
                r_cat = p.add_run(f"{cat_item.category}: ")
                r_cat.font.name = "Arial"
                r_cat.font.size = Pt(9.5)
                r_cat.font.bold = True
                r_cat.font.color.rgb = primary_color
                
                r_skills = p.add_run(", ".join(cat_item.skills))
                r_skills.font.name = "Arial"
                r_skills.font.size = Pt(9.5)
                r_skills.font.color.rgb = text_color
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(" • ".join(resume.skills))
            run.font.name = "Arial"
            run.font.size = Pt(9.5)
            run.font.color.rgb = text_color

    # 5. Professional Experience
    if resume.experience:
        add_section_heading("Professional Experience")
        for exp in resume.experience:
            add_meta_header_row(
                left_title=exp.title,
                left_subtitle=exp.company,
                right_dates=exp.dates,
                right_loc=exp.location or ""
            )

            # Bullets
            for b in exp.bullets:
                bp = doc.add_paragraph(style='List Bullet')
                bp.paragraph_format.left_indent = Inches(0.2)
                bp.paragraph_format.space_before = Pt(1)
                bp.paragraph_format.space_after = Pt(3)
                bp.paragraph_format.line_spacing = 1.15
                brun = bp.add_run(b)
                brun.font.name = "Arial"
                brun.font.size = Pt(9.5)
                brun.font.color.rgb = text_color

    # 6. Key Projects
    if resume.projects:
        add_section_heading("Key Projects")
        for proj in resume.projects:
            subtitle = proj.technologies if proj.technologies else ""
            add_meta_header_row(
                left_title=proj.name,
                left_subtitle=f"({subtitle})" if subtitle else "",
                right_dates=proj.link or ""
            )

            for b in proj.bullets:
                bp = doc.add_paragraph(style='List Bullet')
                bp.paragraph_format.left_indent = Inches(0.2)
                bp.paragraph_format.space_before = Pt(1)
                bp.paragraph_format.space_after = Pt(3)
                bp.paragraph_format.line_spacing = 1.15
                brun = bp.add_run(b)
                brun.font.name = "Arial"
                brun.font.size = Pt(9.5)
                brun.font.color.rgb = text_color

    # 7. Education
    if resume.education:
        add_section_heading("Education")
        for edu in resume.education:
            add_meta_header_row(
                left_title=edu.degree,
                left_subtitle=edu.institution,
                right_dates=edu.dates or ""
            )
            if edu.details:
                dp = doc.add_paragraph()
                dp.paragraph_format.space_before = Pt(0)
                dp.paragraph_format.space_after = Pt(3)
                r_det = dp.add_run(edu.details)
                r_det.font.name = "Arial"
                r_det.font.size = Pt(8.8)
                r_det.font.color.rgb = light_text

    # 8. Certifications
    if resume.certifications:
        add_section_heading("Certifications & Honors")
        for cert in resume.certifications:
            cp = doc.add_paragraph(style='List Bullet')
            cp.paragraph_format.left_indent = Inches(0.2)
            cp.paragraph_format.space_before = Pt(1)
            cp.paragraph_format.space_after = Pt(2.5)
            crun = cp.add_run(cert)
            crun.font.name = "Arial"
            crun.font.size = Pt(9.5)
            crun.font.color.rgb = text_color

    target_io = io.BytesIO()
    doc.save(target_io)
    return target_io.getvalue()


def generate_pdf(resume: ResumeData) -> bytes:
    """
    Generate ATS-friendly, clean, elegant single or multi-page PDF using ReportLab.
    Matches exact margins, printable widths, alignment, and typographic hierarchy of web preview.
    """
    buffer = io.BytesIO()
    
    # 0.55 inch margins (39.6pt)
    margin_pt = 39.6
    page_width_pt = 612.0 # 8.5 inches
    printable_width = page_width_pt - (margin_pt * 2) # 532.8pt
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=margin_pt,
        rightMargin=margin_pt,
        topMargin=margin_pt,
        bottomMargin=margin_pt
    )

    styles = getSampleStyleSheet()

    # Colors
    c_primary = colors.HexColor("#0F172A")    # Deep slate
    c_accent = colors.HexColor("#0284C7")     # Electric Sky/Teal
    c_body = colors.HexColor("#334155")       # Charcoal
    c_muted = colors.HexColor("#64748B")      # Muted slate
    c_line = colors.HexColor("#E2E8F0")       # Border line

    name_style = ParagraphStyle(
        'ResumeName',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        alignment=TA_CENTER
    )

    contact_style = ParagraphStyle(
        'ResumeContact',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_muted,
        alignment=TA_CENTER
    )

    section_style = ParagraphStyle(
        'ResumeSection',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=c_accent,
        spaceBefore=9,
        spaceAfter=2,
        textTransform='uppercase'
    )

    body_style = ParagraphStyle(
        'ResumeBody',
        fontName='Helvetica',
        fontSize=9.2,
        leading=13.5,
        textColor=c_body,
        spaceAfter=4
    )

    skill_category_style = ParagraphStyle(
        'ResumeSkillCategory',
        fontName='Helvetica',
        fontSize=9.2,
        leading=13.5,
        textColor=c_body,
        spaceBefore=1,
        spaceAfter=2.5
    )

    bullet_style = ParagraphStyle(
        'ResumeBullet',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_body,
        leftIndent=14,
        firstLineIndent=-10,
        spaceBefore=1,
        spaceAfter=2.5
    )

    bold_title_style = ParagraphStyle(
        'ResumeItemTitle',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=c_primary
    )

    right_meta_style = ParagraphStyle(
        'ResumeRightMeta',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12.5,
        textColor=c_accent,
        alignment=TA_RIGHT
    )

    elements = []

    # Name
    elements.append(Paragraph(resume.contact.name, name_style))
    elements.append(Spacer(1, 2))

    # Contact Info
    c_items = []
    if resume.contact.email:
        c_items.append(resume.contact.email)
    if resume.contact.phone:
        c_items.append(resume.contact.phone)
    if resume.contact.location:
        c_items.append(resume.contact.location)
    if resume.contact.linkedin:
        c_items.append(resume.contact.linkedin)
    if resume.contact.github:
        c_items.append(resume.contact.github)

    if c_items:
        elements.append(Paragraph(" &nbsp;•&nbsp; ".join(c_items), contact_style))
    elements.append(Spacer(1, 8))

    def add_pdf_section(title: str):
        elements.append(Paragraph(title, section_style))
        elements.append(HRFlowable(width="100%", thickness=1.0, color=c_line, spaceBefore=2, spaceAfter=5))

    # Summary
    if resume.summary:
        add_pdf_section("Professional Summary")
        elements.append(Paragraph(resume.summary, body_style))
        elements.append(Spacer(1, 3))

    # Categorized Core Competencies & Skills
    has_cats = bool(resume.skill_categories)
    has_flat = bool(resume.skills)

    if has_cats or has_flat:
        add_pdf_section("Core Competencies & Technical Skills")
        if has_cats:
            for cat_item in resume.skill_categories:
                skills_str = ", ".join(cat_item.skills)
                line_html = f"<b>{cat_item.category}:</b> {skills_str}"
                elements.append(Paragraph(line_html, skill_category_style))
            elements.append(Spacer(1, 3))
        else:
            skills_text = " &nbsp;•&nbsp; ".join(resume.skills)
            elements.append(Paragraph(skills_text, body_style))
            elements.append(Spacer(1, 3))

    # Experience
    if resume.experience:
        add_pdf_section("Professional Experience")
        for exp in resume.experience:
            left_html = f"<b>{exp.title}</b> &nbsp;|&nbsp; <i>{exp.company}</i>"
            right_html = f"<b>{exp.dates}</b>"
            if exp.location:
                right_html += f" &nbsp;({exp.location})"

            # Dynamic exact 2-column widths summing to printable_width (532.8pt)
            left_w = 380.0
            right_w = printable_width - left_w # 152.8pt
            t = Table(
                [[Paragraph(left_html, bold_title_style), Paragraph(right_html, right_meta_style)]],
                colWidths=[left_w, right_w]
            )
            t.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                ('TOPPADDING', (0,0), (-1,-1), 1),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 2))

            for b in exp.bullets:
                bullet_text = f"&bull; {b}"
                elements.append(Paragraph(bullet_text, bullet_style))

            elements.append(Spacer(1, 4))

    # Projects
    if resume.projects:
        add_pdf_section("Key Projects")
        for proj in resume.projects:
            title_part = f"<b>{proj.name}</b>"
            if proj.technologies:
                title_part += f" <i>({proj.technologies})</i>"
            link_part = f"{proj.link}" if proj.link else ""

            left_w = 370.0
            right_w = printable_width - left_w
            t = Table(
                [[Paragraph(title_part, bold_title_style), Paragraph(link_part, right_meta_style)]],
                colWidths=[left_w, right_w]
            )
            t.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                ('TOPPADDING', (0,0), (-1,-1), 1),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 2))

            for b in proj.bullets:
                elements.append(Paragraph(f"&bull; {b}", bullet_style))
            elements.append(Spacer(1, 4))

    # Education
    if resume.education:
        add_pdf_section("Education")
        for edu in resume.education:
            deg_part = f"<b>{edu.degree}</b> &nbsp;|&nbsp; {edu.institution}"
            date_part = f"<b>{edu.dates}</b>" if edu.dates else ""
            
            left_w = 400.0
            right_w = printable_width - left_w
            t = Table(
                [[Paragraph(deg_part, bold_title_style), Paragraph(date_part, right_meta_style)]],
                colWidths=[left_w, right_w]
            )
            t.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                ('TOPPADDING', (0,0), (-1,-1), 1),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ]))
            elements.append(t)
            if edu.details:
                elements.append(Paragraph(edu.details, ParagraphStyle('EduDet', parent=body_style, fontSize=8.5, textColor=c_muted)))
            elements.append(Spacer(1, 3))

    # Certifications
    if resume.certifications:
        add_pdf_section("Certifications & Honors")
        for cert in resume.certifications:
            elements.append(Paragraph(f"&bull; {cert}", bullet_style))

    doc.build(elements)
    return buffer.getvalue()
