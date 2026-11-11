import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Output Paths
PDF_FILENAME = "25MCA00PY0036_Divyanshu_Yadav.pdf"
PUBLIC_PDF_PATH = os.path.join("frontend", "public", PDF_FILENAME)

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and render total page count 'Page X of Y',
    along with running header and footer rules on all pages except the cover page.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Skip running header and footer on Title/Cover Page
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#1E3A8A"))

        # Running Header
        self.drawString(54, 11 * inch - 36, "SOFTWARE ENGINEERING (MCA) • ASSIGNMENT #01: UML DESIGN DIAGRAMS")
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "VERACITY AI PLATFORM")

        # Top Header Rule
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 11 * inch - 40, 8.5 * inch - 54, 11 * inch - 40)

        # Bottom Footer Rule
        self.line(54, 46, 8.5 * inch - 54, 46)

        # Running Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(54, 34, "Divyanshu Yadav | Roll No: 25MCA00PY0036 | Mini Project Guide: Dr. R. Sunitha")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1E3A8A"))
        self.drawRightString(8.5 * inch - 54, 34, page_str)

        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    c_primary = colors.HexColor("#1E3A8A")   # Deep Academic Navy
    c_secondary = colors.HexColor("#0D9488") # Deep Cyan
    c_dark = colors.HexColor("#0F172A")      # Slate 900
    c_body = colors.HexColor("#334155")      # Slate 700

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=21,
        leading=26,
        textColor=c_primary,
        alignment=1,
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=c_secondary,
        alignment=1,
        spaceAfter=18
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=c_body,
        spaceAfter=7
    )

    body_bold = ParagraphStyle(
        'BodyBoldCustom',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=c_dark
    )

    caption_style = ParagraphStyle(
        'CaptionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=c_primary,
        alignment=1,
        spaceBefore=5,
        spaceAfter=9
    )

    story = []

    # =========================================================
    # 1. FRONT COVER / TITLE PAGE
    # =========================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("DEPARTMENT OF COMPUTER APPLICATIONS", ParagraphStyle('CoverDept', parent=title_style, fontSize=13, leading=16, textColor=c_dark)))
    story.append(Paragraph("MASTER OF COMPUTER APPLICATIONS (MCA)", ParagraphStyle('CoverMCA', parent=title_style, fontSize=11, leading=14, textColor=c_secondary)))
    story.append(Paragraph("COURSE: SOFTWARE ENGINEERING", ParagraphStyle('CoverCourse', parent=title_style, fontSize=10, leading=13, textColor=colors.HexColor("#64748B"))))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=c_primary, spaceBefore=4, spaceAfter=20))

    story.append(Paragraph("ASSIGNMENT #01: COMPLETE SET OF UML DESIGN DIAGRAMS", ParagraphStyle('CoverAssign', parent=title_style, fontSize=12, leading=15, textColor=colors.HexColor("#D97706"))))
    story.append(Spacer(1, 8))

    story.append(Paragraph("VERACITY AI: AI-POWERED MULTI-MODAL MISINFORMATION DETECTION & DIGITAL WELLBEING PLATFORM", title_style))
    story.append(Paragraph("Architectural UML Specification: Use-Case, Class, Sequence, Activity, State, Package, and Deployment Models", subtitle_style))

    story.append(Spacer(1, 15))

    # Student & Submission Metadata Table
    meta_data = [
        [Paragraph("<b>Mini Project Title:</b>", body_style), Paragraph("VERACITY AI: Misinformation Verification & Wellbeing System", body_style)],
        [Paragraph("<b>Student Name:</b>", body_style), Paragraph("<b>DIVYANSHU YADAV</b>", body_bold)],
        [Paragraph("<b>Register / Roll Number:</b>", body_style), Paragraph("<b>25MCA00PY0036</b>", body_bold)],
        [Paragraph("<b>Degree & Program:</b>", body_style), Paragraph("Master of Computer Applications (MCA)", body_style)],
        [Paragraph("<b>Course Name & Code:</b>", body_style), Paragraph("Software Engineering (Assignment #01)", body_style)],
        [Paragraph("<b>Project Guide / Submitted To:</b>", body_style), Paragraph("<b>Dr. R. SUNITHA</b> (Concern Mini Project Guide)", body_bold)],
        [Paragraph("<b>Date of Submission:</b>", body_style), Paragraph("<b>30/10/2026</b>", body_style)],
        [Paragraph("<b>Internal Evaluation Marks:</b>", body_style), Paragraph("<b>10 Marks (Internal Component)</b>", body_bold)],
        [Paragraph("<b>Submission Format:</b>", body_style), Paragraph("Softcopy Document (PDF & Word DOCX Specification)", body_style)],
    ]

    meta_table = Table(meta_data, colWidths=[2.2 * inch, 4.3 * inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1.5, c_primary),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 5.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 25))
    story.append(Paragraph("<i>\"Submitted in partial fulfillment of the academic requirements for the Master of Computer Applications (MCA) Degree in Software Engineering.\"</i>",
                           ParagraphStyle('Cert', parent=body_style, alignment=1, fontSize=8.5, textColor=colors.HexColor("#64748B"))))

    story.append(PageBreak())

    # =========================================================
    # 2. TABLE OF CONTENTS
    # =========================================================
    story.append(Paragraph("TABLE OF CONTENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=2, spaceAfter=10))

    toc_data = [
        [Paragraph("<b>Section</b>", body_bold), Paragraph("<b>Description / Topic</b>", body_bold), Paragraph("<b>Category</b>", body_bold)],
        ["1.0", "Executive Abstract & Problem Definition", "Overview"],
        ["2.0", "System Objectives & Engineering Scope", "Requirements"],
        ["3.0", "Technical Architecture & Component Stack", "System Design"],
        ["4.0", "UML Diagram 1: Use-Case Diagram & Functional Requirements", "Behavioral Model"],
        ["5.0", "UML Diagram 2: Class Diagram & Domain Object Model", "Structural Model"],
        ["6.0", "UML Diagram 3: Sequence Diagram & Dynamic Message Passing", "Interaction Model"],
        ["7.0", "UML Diagram 4: Activity Diagram & Operational Workflows", "Process Model"],
        ["8.0", "UML Diagram 5: State Machine Diagram & Object Lifecycles", "Dynamic State Model"],
        ["9.0", "UML Diagram 6: Package Diagram & Modular Subsystems", "Architectural Model"],
        ["10.0", "UML Diagram 7: Component & Deployment Diagram", "Physical Implementation"],
        ["11.0", "Software Engineering Evaluation & Conclusion", "Summary"]
    ]

    toc_table = Table(toc_data, colWidths=[0.8 * inch, 4.4 * inch, 1.6 * inch])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(toc_table)

    story.append(Spacer(1, 15))

    # =========================================================
    # 3. EXECUTIVE ABSTRACT
    # =========================================================
    story.append(Paragraph("1.0 EXECUTIVE ABSTRACT & PROBLEM DEFINITION", h1_style))
    story.append(Paragraph(
        "The exponential expansion of digital news channels, social networking ecosystems, and online forums has magnified the velocity and volume at which unverified rumors, fabricated stories, and coordinated misinformation proliferate. Concurrently, excessive screen time and smartphone dependency have precipitated widespread digital fatigue, reduced cognitive attention spans, and diminished user productivity. To comprehensively address these two interconnected digital challenges, this project presents <b>VERACITY AI</b>, an integrated software platform engineered to perform automated, multi-modal misinformation detection alongside native hardware screen-time monitoring and AI-synthesized digital wellbeing recommendations.",
        body_style
    ))
    story.append(Paragraph(
        "<b>VERACITY AI</b> leverages a hybrid artificial intelligence pipeline combining Google Gemini 1.5 generative models, Scikit-Learn TF-IDF lexical signal classifiers, and automated domain credibility registries. Simultaneously, the platform monitors local Windows OS telemetry via native Win32 kernel APIs (<code>GetTickCount64</code>, <code>GetLastInputInfo</code>) and Android companion sync (<code>UsageStatsManager</code>) to compute dynamic productivity indices and trigger personalized habit interventions (e.g., 20-20-20 screen relief, app timers). This document establishes the formal Software Engineering Unified Modeling Language (UML) design artifacts governing the platform's architectural blueprint, structural relationships, behavioral sequences, and physical deployment boundaries.",
        body_style
    ))

    story.append(Spacer(1, 6))

    # =========================================================
    # 4. SYSTEM OBJECTIVES & ARCHITECTURE
    # =========================================================
    story.append(Paragraph("2.0 SYSTEM OBJECTIVES & ENGINEERING SPECIFICATION", h1_style))
    obj_data = [
        [Paragraph("<b>Objective ID</b>", body_bold), Paragraph("<b>Software Engineering Objective</b>", body_bold), Paragraph("<b>Target Module / Implementation</b>", body_bold)],
        ["OBJ-01", "Automated Fact Verification", "Gemini 1.5 Flash API + TF-IDF Credibility Scoring"],
        ["OBJ-02", "Domain Credibility Analysis", "URL Whitelist / Journalistic Source Assessment Registry"],
        ["OBJ-03", "Conversational Media Literacy", "Interactive AI Chatbot explaining disinformation heuristics"],
        ["OBJ-04", "Operating System Telemetry", "Win32 Kernel32/User32 + Android UsageStatsManager"],
        ["OBJ-05", "Dynamic Productivity Scoring", "Algorithmic ratio of work tools vs distracting social media"],
        ["OBJ-06", "Habit Intelligence Engine", "Generative synthesis of personalized digital health advice"],
        ["OBJ-07", "Enterprise Analytics", "Looker Studio Embed + REST API aggregation dashboards"]
    ]
    obj_table = Table(obj_data, colWidths=[1.1 * inch, 3.2 * inch, 2.5 * inch])
    obj_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0D9488")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F0FDFA")]),
    ]))
    story.append(obj_table)

    story.append(PageBreak())

    # =========================================================
    # 5. DIAGRAM 1: USE CASE DIAGRAM
    # =========================================================
    story.append(Paragraph("4.0 UML DIAGRAM 1: USE-CASE DIAGRAM", h1_style))
    story.append(Paragraph("<b>Subtitle:</b> Behavioral Functional Scope and Actor-System Interactions in Veracity AI", h2_style))
    story.append(Paragraph(
        "The Use-Case Diagram depicts the functional boundary of the Veracity AI platform, defining how external human actors and autonomous cloud agents interact with core system functions. The system boundary encapsulates seven critical use-case clusters ranging from authentication to AI fact-checking and OS telemetry ingestion.",
        body_style
    ))

    diag_1_path = os.path.join("scratch", "uml_diagrams", "01_use_case_diagram.png")
    if os.path.exists(diag_1_path):
        story.append(Image(diag_1_path, width=6.5 * inch, height=4.6 * inch))
        story.append(Paragraph("<b>Figure 4.1:</b> UML Use-Case Diagram for Veracity AI Misinformation & Wellbeing Platform", caption_style))

    story.append(Paragraph("<b>Detailed Architectural Breakdown of Actors & Use Cases:</b>", body_bold))
    uc_desc = [
        [Paragraph("<b>Entity / Actor</b>", body_bold), Paragraph("<b>Type</b>", body_bold), Paragraph("<b>Role & Interaction Description</b>", body_bold)],
        ["User / Student", "Primary Human", "Submits claims, checks source URLs, queries AI verifier chatbot, and monitors personal laptop/phone screen time."],
        ["Fact-Checker / Admin", "Secondary Human", "Validates flagged discrepancies, inspects systemic verdict analytics, and oversees verification integrity."],
        ["Google Gemini AI", "External Cloud Actor", "Receives grounded verification prompts via REST/TLS 1.3; outputs structured verdicts, scores, and citations."],
        ["OS Telemetry Provider", "Native System Actor", "Extracts Windows kernel uptime (GetTickCount64), active typing intervals, and Android UsageStats data."]
    ]
    uc_table = Table(uc_desc, colWidths=[1.5 * inch, 1.2 * inch, 4.1 * inch])
    uc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(uc_table)

    story.append(PageBreak())

    # =========================================================
    # 6. DIAGRAM 2: CLASS DIAGRAM
    # =========================================================
    story.append(Paragraph("5.0 UML DIAGRAM 2: CLASS DIAGRAM", h1_style))
    story.append(Paragraph("<b>Subtitle:</b> Static Domain Object Model, Class Compartments, and Structural Associations", h2_style))
    story.append(Paragraph(
        "The Class Diagram models the static structural backbone of Veracity AI, detailing domain entities, encapsulation boundaries, attributes with explicit data types, public/private methods, and inter-class relationships including composition, inheritance, and multiplicity constraints.",
        body_style
    ))

    diag_2_path = os.path.join("scratch", "uml_diagrams", "02_class_diagram.png")
    if os.path.exists(diag_2_path):
        story.append(Image(diag_2_path, width=6.6 * inch, height=4.8 * inch))
        story.append(Paragraph("<b>Figure 5.1:</b> UML Class Diagram representing OOP Domain Architecture and ORM Entities", caption_style))

    story.append(Paragraph("<b>Class Responsibilities and Relationships:</b>", body_bold))
    story.append(Paragraph(
        "• <b>User & UserProfile:</b> Represents system identity with 1-to-1 association. Captures registered researcher metadata (Roll No: 25MCA00PY0036) and hardware profile.<br/>"
        "• <b>VerificationCheck & NLPEngine:</b> Encapsulates news claims, verdict enumerations (<code>TRUE</code>, <code>FALSE</code>, <code>MISLEADING</code>, <code>UNVERIFIED</code>), confidence floats, and citations. Dependent on <code>NLPEngine</code> for feature tokenization.<br/>"
        "• <b>ScreenTimeRecord & AppUsageRecord:</b> Models cumulative daily screen duration with 1-to-many composition. Automatically computes productivity scores based on active app category breakdown.<br/>"
        "• <b>LaptopMonitor:</b> Interfaces directly with Windows kernel32/user32 APIs to extract native hardware telemetry without external invasive dependencies.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================
    # 7. DIAGRAM 3: SEQUENCE DIAGRAM
    # =========================================================
    story.append(Paragraph("6.0 UML DIAGRAM 3: SEQUENCE DIAGRAM", h1_style))
    story.append(Paragraph("<b>Subtitle:</b> Chronological Message Flow for Multi-Modal Claim Verification and Persistence", h2_style))
    story.append(Paragraph(
        "The Sequence Diagram captures the chronological order of message exchanges among the Client Browser, React Presentation Layer, Django REST Controller, AI Processing Engine, and MySQL Persistence Engine during an end-to-end fact-checking transaction.",
        body_style
    ))

    diag_3_path = os.path.join("scratch", "uml_diagrams", "03_sequence_diagram.png")
    if os.path.exists(diag_3_path):
        story.append(Image(diag_3_path, width=6.6 * inch, height=4.7 * inch))
        story.append(Paragraph("<b>Figure 6.1:</b> UML Sequence Diagram demonstrating Real-Time Claim Verification and Screen Logging", caption_style))

    story.append(Paragraph("<b>Chronological Execution Steps:</b>", body_bold))
    story.append(Paragraph(
        "<b>1. Initiation:</b> User submits news claim text and source URL through the React UI (<code>QuickCheck.jsx</code>).<br/>"
        "<b>2. Dispatch:</b> React dispatches an asynchronous HTTP POST request to Django endpoint <code>/api/verify/</code>.<br/>"
        "<b>3. NLP Preprocessing:</b> Controller activates <code>NLPEngine</code> to generate TF-IDF linguistic signal vectors and check domain whitelists.<br/>"
        "<b>4. AI Reasoning:</b> Controller constructs a grounded prompt dispatched to Google Gemini 1.5 API via TLS 1.3.<br/>"
        "<b>5. Synthesis & Storage:</b> Gemini returns structured JSON verdict with confidence score and evidence quotes, persisted into MySQL.<br/>"
        "<b>6. Telemetry Feedback:</b> Active laptop session duration is updated, and personalized habit guidance is refreshed.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================
    # 8. DIAGRAM 4: ACTIVITY DIAGRAM
    # =========================================================
    story.append(Paragraph("7.0 UML DIAGRAM 4: ACTIVITY DIAGRAM", h1_style))
    story.append(Paragraph("<b>Subtitle:</b> Operational Logic, Decision Branches, and Concurrent Task Synchronization", h2_style))
    story.append(Paragraph(
        "The Activity Diagram formalizes the operational decision tree and parallel data processing pipelines within Veracity AI. It models control flow from input ingestion through concurrent algorithmic evaluation to automated wellbeing habit intervention.",
        body_style
    ))

    diag_4_path = os.path.join("scratch", "uml_diagrams", "04_activity_diagram.png")
    if os.path.exists(diag_4_path):
        story.append(Image(diag_4_path, width=5.6 * inch, height=5.2 * inch))
        story.append(Paragraph("<b>Figure 7.1:</b> UML Activity Diagram illustrating Verification Fork/Join & Break Scheduling", caption_style))

    story.append(Paragraph("<b>Core Workflow Logic & Synchronization Points:</b>", body_bold))
    story.append(Paragraph(
        "• <b>Input Validation Decision:</b> Verifies string non-emptiness; rejects invalid payloads with immediate client notification.<br/>"
        "• <b>Parallel Fork Bar:</b> Simultaneously executes local Scikit-Learn TF-IDF lexical classification and external Google Gemini AI fact retrieval.<br/>"
        "• <b>Synchronization Join Bar:</b> Aggregates multi-modal signals to compute a weighted confidence index.<br/>"
        "• <b>Wellbeing Branch:</b> Evaluates continuous laptop focus timer; if active session exceeds 45 minutes, automatically schedules a 20-20-20 screen relief notification.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================
    # 9. DIAGRAM 5: STATE MACHINE DIAGRAM
    # =========================================================
    story.append(Paragraph("8.0 UML DIAGRAM 5: STATE MACHINE DIAGRAM", h1_style))
    story.append(Paragraph("<b>Subtitle:</b> Object State Transitions: Verification Lifecycle & Digital Wellbeing Modes", h2_style))
    story.append(Paragraph(
        "The State Machine Diagram illustrates dynamic object lifecycles across discrete system states. It comprises two complementary sub-diagrams: (A) Claim Verification Lifecycle, and (B) Digital Wellbeing Operating States.",
        body_style
    ))

    diag_5_path = os.path.join("scratch", "uml_diagrams", "05_state_diagram.png")
    if os.path.exists(diag_5_path):
        story.append(Image(diag_5_path, width=6.5 * inch, height=4.8 * inch))
        story.append(Paragraph("<b>Figure 8.1:</b> UML State Machine Diagram showing Claim Lifecycle & Screen Wellbeing Transitions", caption_style))

    story.append(Paragraph("<b>State Transition Semantics:</b>", body_bold))
    story.append(Paragraph(
        "• <b>Claim Verification States:</b> Transitions from <code>Submitted</code> to <code>Processing</code> (tokenization), <code>Evaluating</code> (Gemini inference), <code>Verdicted</code> (assigned verdict), and finally <code>Archived</code> in the historical audit index.<br/>"
        "• <b>Wellbeing States:</b> Starts at <code>System Booted</code>. User activity transitions the system into <code>Active Focused</code>. When <code>idle_seconds > 180</code>, transitions to <code>Idle / Paused</code>. If active focus surpasses 45 continuous minutes, transitions to <code>Extended Strain</code> until user adopts habit advice, restoring <code>Break Restored</code>.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================
    # 10. DIAGRAM 6: PACKAGE DIAGRAM
    # =========================================================
    story.append(Paragraph("9.0 UML DIAGRAM 6: PACKAGE DIAGRAM", h1_style))
    story.append(Paragraph("<b>Subtitle:</b> Multi-Tier Modular Subsystem Architecture and Inter-Package Dependencies", h2_style))
    story.append(Paragraph(
        "The Package Diagram organizes the classes and software artifacts of Veracity AI into coherent, loosely-coupled logical packages adhering to clean architecture principles.",
        body_style
    ))

    diag_6_path = os.path.join("scratch", "uml_diagrams", "06_package_diagram.png")
    if os.path.exists(diag_6_path):
        story.append(Image(diag_6_path, width=6.5 * inch, height=4.7 * inch))
        story.append(Paragraph("<b>Figure 9.1:</b> UML Package Diagram detailing Modular Layered Organization", caption_style))

    story.append(Paragraph("<b>Package Responsibilities:</b>", body_bold))
    story.append(Paragraph(
        "1. <b>com.veracity.presentation:</b> Next.js 16 / React 19 UI components including Rumours Feed, Quick Check, and 3D Canvas visualizers.<br/>"
        "2. <b>com.veracity.api_controllers:</b> Django REST Framework endpoint viewsets governing authentication, verification, and telemetry ingestion.<br/>"
        "3. <b>com.veracity.ai_intelligence:</b> Encapsulates Google Gemini AI wrappers, Scikit-Learn TF-IDF classifiers, and recommendation synthesis.<br/>"
        "4. <b>com.veracity.telemetry:</b> Interfaces with Windows Win32 OS APIs and Android UsageStatsManager data models.<br/>"
        "5. <b>com.veracity.data_persistence:</b> Django ORM models managing relational mapping to MySQL / SQLite.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================
    # 11. DIAGRAM 7: DEPLOYMENT DIAGRAM
    # =========================================================
    story.append(Paragraph("10.0 UML DIAGRAM 7: COMPONENT & DEPLOYMENT DIAGRAM", h1_style))
    story.append(Paragraph("<b>Subtitle:</b> Physical Hardware Nodes, Execution Environments, Artifacts, and Protocols", h2_style))
    story.append(Paragraph(
        "The Deployment Diagram visualizes the physical infrastructure topology, hardware nodes, software execution environments, deployed artifacts, and communication protocols connecting client devices to cloud services.",
        body_style
    ))

    diag_7_path = os.path.join("scratch", "uml_diagrams", "07_component_deployment_diagram.png")
    if os.path.exists(diag_7_path):
        story.append(Image(diag_7_path, width=6.5 * inch, height=4.7 * inch))
        story.append(Paragraph("<b>Figure 10.1:</b> UML Deployment Diagram depicting Node Topology and Protocol Mapping", caption_style))

    story.append(Paragraph("<b>Hardware Nodes & Deployed Artifacts:</b>", body_bold))
    story.append(Paragraph(
        "• <b>Client Workstation:</b> Windows 11 host executing Web Browser (Chrome/Edge on Port 3000) and native OS background telemetry agent.<br/>"
        "• <b>Next.js Web Server:</b> Node.js runtime executing the React 19 production bundle.<br/>"
        "• <b>Django Backend Server:</b> Python 3.14 runtime hosting Django REST Framework API on Port 8000.<br/>"
        "• <b>Relational Database:</b> MySQL / SQLite 3 database storing user profiles, claims, and telemetry history.<br/>"
        "• <b>External Cloud Service:</b> Google Cloud Generative AI endpoint communicating via secure HTTPS/TLS 1.3.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================
    # 12. CONCLUSION & SE PRINCIPLES
    # =========================================================
    story.append(Paragraph("11.0 SOFTWARE ENGINEERING PRINCIPLES & CONCLUSION", h1_style))
    story.append(Paragraph(
        "The architectural design of <b>VERACITY AI</b> demonstrates rigorous adherence to foundational Software Engineering tenets, ensuring robustness, extensibility, and maintainability across its software lifecycle:",
        body_style
    ))
    story.append(Paragraph(
        "<b>1. Separation of Concerns (SoC):</b> Decoupling the frontend presentation layer (Next.js), REST API routing (Django), machine learning reasoning (Gemini/Scikit-Learn), and hardware telemetry ensures that modifications to one tier do not ripple unpredictably into others.<br/>"
        "<b>2. High Cohesion & Loose Coupling:</b> Packages encapsulate logically related functionality with clean, protocol-driven interfaces (REST JSON over HTTP).<br/>"
        "<b>3. Modularity & Scalability:</b> Independent deployment of the Next.js web tier and Django API server facilitates horizontal scaling across distributed cloud clusters.<br/>"
        "<b>4. Privacy by Design:</b> Hardware monitoring strictly reads OS process names and uptime counters via native Win32 APIs without accessing personal emails or private files.",
        body_style
    ))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=4, spaceAfter=14))

    # Signature Block
    sig_data = [
        [Paragraph("<b>Student Signature:</b>", body_style), Paragraph("<b>Faculty Guide Signature:</b>", body_style)],
        [Spacer(1, 18), Spacer(1, 18)],
        [Paragraph("<b>DIVYANSHU YADAV</b><br/>Roll No: 25MCA00PY0036<br/>MCA Final Project Student", body_style),
         Paragraph("<b>Dr. R. SUNITHA</b><br/>Project Guide & Evaluator<br/>Department of Computer Applications", body_style)]
    ]
    sig_table = Table(sig_data, colWidths=[3.3 * inch, 3.3 * inch])
    sig_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(sig_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF built successfully at: {filename}")

if __name__ == '__main__':
    build_pdf(PDF_FILENAME)
    # Also copy to frontend public directory
    import shutil
    shutil.copyfile(PDF_FILENAME, PUBLIC_PDF_PATH)
    print(f"Copied to public web path: {PUBLIC_PDF_PATH}")
