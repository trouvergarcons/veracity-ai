import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

DOCX_FILENAME = "25MCA00PY0036_Divyanshu_Yadav.docx"
PUBLIC_DOCX_PATH = os.path.join("frontend", "public", DOCX_FILENAME)

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def create_docx(filename):
    doc = docx.Document()

    # Set 0.75 inch margins
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.75)
        s.bottom_margin = Inches(0.75)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)

    c_primary = RGBColor(30, 58, 138)    # Navy
    c_secondary = RGBColor(13, 148, 136) # Cyan
    c_dark = RGBColor(15, 23, 42)        # Slate 900
    c_body = RGBColor(51, 65, 85)        # Slate 700

    # =========================================================
    # 1. TITLE / COVER PAGE
    # =========================================================
    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_dept.add_run("DEPARTMENT OF COMPUTER APPLICATIONS\nMASTER OF COMPUTER APPLICATIONS (MCA)\nCOURSE: SOFTWARE ENGINEERING")
    r.font.name = "Arial"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = c_primary

    p_assign = doc.add_paragraph()
    p_assign.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_assign = p_assign.add_run("\nASSIGNMENT #01: COMPLETE SET OF UML DESIGN DIAGRAMS")
    r_assign.font.name = "Arial"
    r_assign.font.size = Pt(12)
    r_assign.font.bold = True
    r_assign.font.color.rgb = RGBColor(217, 119, 6)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("\nVERACITY AI: AI-POWERED MULTI-MODAL MISINFORMATION DETECTION & DIGITAL WELLBEING PLATFORM\n")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = c_primary

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Comprehensive Software Engineering Design Specification & UML Architectural Models\n")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(10.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = c_secondary

    # Metadata Table
    meta_table = doc.add_table(rows=8, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_rows = [
        ("Mini Project Title:", "VERACITY AI: Misinformation Verification & Wellbeing System"),
        ("Student Name:", "DIVYANSHU YADAV"),
        ("Register / Roll Number:", "25MCA00PY0036"),
        ("Degree & Course:", "Master of Computer Applications (MCA)"),
        ("Subject Name:", "Software Engineering (Assignment #01)"),
        ("Project Guide / Evaluator:", "Dr. R. SUNITHA (Concern Mini Project Guide)"),
        ("Date of Submission:", "30/10/2026"),
        ("Marks Weightage:", "10 Marks (Internal Component)")
    ]

    for i, (k, v) in enumerate(meta_rows):
        row = meta_table.rows[i]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width = Inches(2.2)
        c2.width = Inches(4.3)
        c1.paragraphs[0].add_run(k).bold = True
        c2.paragraphs[0].add_run(v).bold = (i in [1, 2, 5, 7])
        set_cell_background(c1, "F8FAFC")
        set_cell_background(c2, "F8FAFC")

    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_foot = p_foot.add_run("\n\n\"Submitted in partial fulfillment of the academic requirements for the Master of Computer Applications (MCA) Degree in Software Engineering.\"")
    r_foot.font.italic = True
    r_foot.font.size = Pt(8.5)
    r_foot.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # =========================================================
    # 2. TABLE OF CONTENTS & ABSTRACT
    # =========================================================
    p_toc_head = doc.add_heading("TABLE OF CONTENTS", level=1)
    p_toc_head.runs[0].font.color.rgb = c_primary

    toc_items = [
        ("1.0", "Executive Abstract & Problem Definition", "Overview"),
        ("2.0", "System Objectives & Engineering Specification", "Requirements"),
        ("3.0", "Technical Architecture & Component Stack", "System Design"),
        ("4.0", "UML Diagram 1: Use-Case Diagram & Functional Requirements", "Behavioral Model"),
        ("5.0", "UML Diagram 2: Class Diagram & Domain Object Model", "Structural Model"),
        ("6.0", "UML Diagram 3: Sequence Diagram & Dynamic Message Passing", "Interaction Model"),
        ("7.0", "UML Diagram 4: Activity Diagram & Operational Workflows", "Process Model"),
        ("8.0", "UML Diagram 5: State Machine Diagram & Object Lifecycles", "Dynamic State Model"),
        ("9.0", "UML Diagram 6: Package Diagram & Modular Subsystems", "Architectural Model"),
        ("10.0", "UML Diagram 7: Component & Deployment Diagram", "Physical Implementation"),
        ("11.0", "Software Engineering Evaluation & Conclusion", "Summary")
    ]

    t_toc = doc.add_table(rows=len(toc_items) + 1, cols=3)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_row = t_toc.rows[0]
    h_row.cells[0].paragraphs[0].add_run("Section").bold = True
    h_row.cells[1].paragraphs[0].add_run("Topic / Description").bold = True
    h_row.cells[2].paragraphs[0].add_run("Category").bold = True
    for c in h_row.cells:
        set_cell_background(c, "1E3A8A")
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    for idx, item in enumerate(toc_items):
        r = t_toc.rows[idx + 1]
        r.cells[0].paragraphs[0].add_run(item[0])
        r.cells[1].paragraphs[0].add_run(item[1])
        r.cells[2].paragraphs[0].add_run(item[2])
        if idx % 2 == 1:
            for cell in r.cells:
                set_cell_background(cell, "F8FAFC")

    # Abstract Section
    p_abs_head = doc.add_heading("\n1.0 EXECUTIVE ABSTRACT & PROBLEM DEFINITION", level=1)
    p_abs_head.runs[0].font.color.rgb = c_primary

    p_abs1 = doc.add_paragraph(
        "The rapid expansion of social media and online content distribution has dramatically accelerated the spread of unverified claims and fake news, impairing public discourse. In tandem, excessive smartphone and laptop usage leads to digital strain, eye fatigue, and reduced cognitive performance. VERACITY AI is an integrated platform combining multi-modal fake news verification with native hardware screen-time monitoring and generative AI habit coaching."
    )
    p_abs2 = doc.add_paragraph(
        "The platform utilizes Google Gemini AI coupled with local Scikit-Learn TF-IDF classifiers for fact-checking, while simultaneously extracting native Windows OS metrics (GetTickCount64, GetLastInputInfo) and Android UsageStatsManager telemetry. This Software Engineering document presents the complete set of UML design models governing the platform's architectural, behavioral, and physical deployment structure."
    )

    doc.add_page_break()

    # =========================================================
    # 3. UML DIAGRAMS 1 TO 7
    # =========================================================
    diagrams = [
        {
            "num": "4.0",
            "name": "UML DIAGRAM 1: USE-CASE DIAGRAM",
            "subtitle": "Behavioral Functional Scope and Actor-System Interactions in Veracity AI",
            "img": "scratch/uml_diagrams/01_use_case_diagram.png",
            "caption": "Figure 4.1: UML Use-Case Diagram for Veracity AI Platform",
            "desc": "The Use-Case diagram establishes the functional boundaries of the system. Four key actors interact with the core platform: the User/Student (submitting claims and viewing screen time), the Administrator/Fact-Checker (overseeing verification audits), the Google Gemini AI Cloud Service (generating evidence-grounded verdicts), and the Native OS Telemetry API (ingesting Win32 and Android usage metrics)."
        },
        {
            "num": "5.0",
            "name": "UML DIAGRAM 2: CLASS DIAGRAM",
            "subtitle": "Static Domain Object Model, Class Compartments, and Structural Associations",
            "img": "scratch/uml_diagrams/02_class_diagram.png",
            "caption": "Figure 5.1: UML Class Diagram representing OOP Domain Architecture and ORM Entities",
            "desc": "The Class diagram visualizes the object-oriented structure of Veracity AI. Key classes include User and UserProfile (1-to-1 auth and student identity), VerificationCheck (encapsulating claim text, verdict enum, and confidence float), NLPEngine (handling TF-IDF vectorization and Gemini API calls), ScreenTimeRecord with AppUsageRecord composition, and LaptopMonitor (interfacing with Win32 kernel32/user32)."
        },
        {
            "num": "6.0",
            "name": "UML DIAGRAM 3: SEQUENCE DIAGRAM",
            "subtitle": "Chronological Message Flow for Multi-Modal Claim Verification and Persistence",
            "img": "scratch/uml_diagrams/03_sequence_diagram.png",
            "caption": "Figure 6.1: UML Sequence Diagram demonstrating Real-Time Claim Verification and Screen Logging",
            "desc": "The Sequence diagram details the chronological message passing across lifelines: Client User -> React 19 Frontend -> Django REST API -> NLP / Scikit Engine -> Google Gemini 1.5 Cloud -> MySQL Database. It highlights asynchronous HTTP POST dispatching, structured JSON response synthesis, and live telemetry logging."
        },
        {
            "num": "7.0",
            "name": "UML DIAGRAM 4: ACTIVITY DIAGRAM",
            "subtitle": "Operational Logic, Decision Branches, and Concurrent Task Synchronization",
            "img": "scratch/uml_diagrams/04_activity_diagram.png",
            "caption": "Figure 7.1: UML Activity Diagram illustrating Verification Fork/Join & Break Scheduling",
            "desc": "The Activity diagram formalizes control flow through the system. It models input validation decision diamonds, parallel fork bars executing concurrent Scikit-learn TF-IDF analysis and Gemini AI grounded verification, join synchronization, database persistence, and automated conditional branching for screen breaks if active focus exceeds 45 minutes."
        },
        {
            "num": "8.0",
            "name": "UML DIAGRAM 5: STATE MACHINE DIAGRAM",
            "subtitle": "Object State Transitions: Verification Lifecycle & Digital Wellbeing Modes",
            "img": "scratch/uml_diagrams/05_state_diagram.png",
            "caption": "Figure 8.1: UML State Machine Diagram showing Claim Lifecycle & Screen Wellbeing Transitions",
            "desc": "The State Machine diagram illustrates discrete state transitions for two core domains: (A) Claim Verification Lifecycle from Submitted to Processing, Evaluating, Verdicted (True/False/Misleading), and Archived; and (B) Digital Wellbeing States transitioning between System Booted, Active Focused, Idle / Paused, and Extended Screen Strain."
        },
        {
            "num": "9.0",
            "name": "UML DIAGRAM 6: PACKAGE DIAGRAM",
            "subtitle": "Multi-Tier Modular Subsystem Architecture and Inter-Package Dependencies",
            "img": "scratch/uml_diagrams/06_package_diagram.png",
            "caption": "Figure 9.1: UML Package Diagram detailing Modular Layered Organization",
            "desc": "The Package diagram structures the application into layered, loosely-coupled packages: com.veracity.presentation (Next.js / React UI), com.veracity.api_controllers (Django REST Framework viewsets), com.veracity.ai_intelligence (Gemini and Scikit ML), com.veracity.telemetry (Win32 OS & Android bridge), and com.veracity.data_persistence (Django ORM & MySQL)."
        },
        {
            "num": "10.0",
            "name": "UML DIAGRAM 7: COMPONENT & DEPLOYMENT DIAGRAM",
            "subtitle": "Physical Hardware Nodes, Execution Environments, Artifacts, and Protocols",
            "img": "scratch/uml_diagrams/07_component_deployment_diagram.png",
            "caption": "Figure 10.1: UML Deployment Diagram depicting Node Topology and Protocol Mapping",
            "desc": "The Deployment diagram visualizes physical execution nodes and communication protocols: Client Workstation executing Chrome/Edge, Next.js Web Server (Port 3000), Django REST Backend (Port 8000), MySQL Relational Database Engine (TCP 3306), and Google Cloud Gemini API Server (HTTPS / TLS 1.3)."
        }
    ]

    for d in diagrams:
        h = doc.add_heading(f"{d['num']} {d['name']}", level=1)
        h.runs[0].font.color.rgb = c_primary

        p_sub = doc.add_paragraph()
        r_sub = p_sub.add_run(f"Subtitle: {d['subtitle']}")
        r_sub.font.bold = True
        r_sub.font.color.rgb = c_secondary

        doc.add_paragraph(d['desc'])

        if os.path.exists(d['img']):
            doc.add_picture(d['img'], width=Inches(6.2))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_cap = p_cap.add_run(d['caption'])
            r_cap.font.bold = True
            r_cap.font.size = Pt(8.5)
            r_cap.font.color.rgb = c_primary

        doc.add_page_break()

    # =========================================================
    # 4. CONCLUSION
    # =========================================================
    p_conc = doc.add_heading("11.0 SOFTWARE ENGINEERING PRINCIPLES & CONCLUSION", level=1)
    p_conc.runs[0].font.color.rgb = c_primary

    doc.add_paragraph(
        "The software architecture of VERACITY AI adheres to fundamental Software Engineering tenets, including Separation of Concerns (SoC), High Cohesion and Loose Coupling, Privacy by Design, and Modularity. By thoroughly capturing these architectural decisions in the complete suite of UML Design Diagrams, the system is fully specified for reliable deployment, rigorous maintenance, and academic assessment."
    )

    p_sig = doc.add_paragraph("\n\n")
    p_sig.add_run("Submitted By:\n").bold = True
    p_sig.add_run("DIVYANSHU YADAV\nRoll Number: 25MCA00PY0036\nMaster of Computer Applications (MCA)\n\n")
    p_sig.add_run("Mini Project Guide:\n").bold = True
    p_sig.add_run("Dr. R. SUNITHA\nDepartment of Computer Applications\nDate: 30/10/2026")

    doc.save(filename)
    print(f"DOCX built successfully at: {filename}")

if __name__ == '__main__':
    create_docx(DOCX_FILENAME)
    import shutil
    shutil.copyfile(DOCX_FILENAME, PUBLIC_DOCX_PATH)
    print(f"Copied to public web path: {PUBLIC_DOCX_PATH}")
