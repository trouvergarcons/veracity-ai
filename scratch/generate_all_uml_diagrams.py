import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('scratch/uml_diagrams', exist_ok=True)

# -------------------------------------------------------------
# 1. USE CASE DIAGRAM
# -------------------------------------------------------------
def generate_use_case():
    fig, ax = plt.subplots(figsize=(11, 8.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # System Boundary Box
    system_box = patches.FancyBboxPatch((24, 4), 52, 92, boxstyle="round,pad=1.5",
                                        facecolor='#F8FAFC', edgecolor='#1E3A8A', linewidth=2.5)
    ax.add_patch(system_box)
    ax.text(50, 93, "VERACITY AI PLATFORM (SYSTEM BOUNDARY)", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#1E3A8A')

    # Actors
    def draw_actor(x, y, name, role):
        head = patches.Circle((x, y + 4), 2.2, facecolor='#E2E8F0', edgecolor='#0F172A', linewidth=1.8)
        ax.add_patch(head)
        ax.plot([x, x], [y + 1.8, y - 3.5], color='#0F172A', lw=2)
        ax.plot([x - 2.8, x + 2.8], [y + 0.2, y + 0.2], color='#0F172A', lw=2)
        ax.plot([x, x - 2.5], [y - 3.5, y - 7.5], color='#0F172A', lw=2)
        ax.plot([x, x + 2.5], [y - 3.5, y - 7.5], color='#0F172A', lw=2)
        ax.text(x, y - 10, name, ha='center', va='top', fontsize=9, fontweight='bold', color='#0F172A')
        ax.text(x, y - 12.2, f"({role})", ha='center', va='top', fontsize=7.5, color='#475569')

    draw_actor(11, 72, "User / Student", "Primary Actor")
    draw_actor(11, 28, "Fact-Checker / Admin", "Secondary Actor")
    draw_actor(89, 72, "Google Gemini AI", "External AI Service")
    draw_actor(89, 28, "OS & Telemetry API", "Win32 / Android")

    # Use Cases
    use_cases = [
        ("UC1: User Authentication & Profile Security", 50, 85, '#E0F2FE', '#0284C7'),
        ("UC2: Submit News Claim & Article Text", 50, 73, '#E0F2FE', '#0284C7'),
        ("UC3: Submit URL for Domain Credibility Check", 50, 61, '#E0F2FE', '#0284C7'),
        ("UC4: Real-Time Multi-Modal AI Verification", 50, 49, '#FEF3C7', '#D97706'),
        ("UC5: Consult AI Chatbot for Media Literacy", 50, 37, '#E0F2FE', '#0284C7'),
        ("UC6: Track Laptop Screen Time & OS Sensors", 50, 25, '#DCFCE7', '#16A34A'),
        ("UC7: View Digital Habits & AI Recommendations", 50, 13, '#DCFCE7', '#16A34A')
    ]

    for text, cx, cy, bg, border in use_cases:
        ellipse = patches.Ellipse((cx, cy), 31, 7.8, facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(ellipse)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=8, fontweight='semibold', color='#0F172A')

    # Association lines
    for target in [(34, 85), (34, 73), (34, 61), (34, 37), (34, 25), (34, 13)]:
        ax.annotate("", xy=target, xytext=(15, 70), arrowprops=dict(arrowstyle="-", color='#334155', lw=1.2))

    for target in [(34, 85), (34, 49), (34, 13)]:
        ax.annotate("", xy=target, xytext=(15, 28), arrowprops=dict(arrowstyle="-", color='#334155', lw=1.2))

    for target in [(66, 49), (66, 37), (66, 13)]:
        ax.annotate("", xy=target, xytext=(85, 70), arrowprops=dict(arrowstyle="-", color='#D97706', lw=1.3, linestyle="--"))

    for target in [(66, 25), (66, 13)]:
        ax.annotate("", xy=target, xytext=(85, 28), arrowprops=dict(arrowstyle="-", color='#16A34A', lw=1.3, linestyle="--"))

    # Include relationships
    ax.annotate("«include»", xy=(50, 53), xytext=(50, 69),
                arrowprops=dict(arrowstyle="->", color='#0284C7', lw=1.2, linestyle=":"),
                ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0284C7')

    plt.tight_layout()
    plt.savefig('scratch/uml_diagrams/01_use_case_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

# -------------------------------------------------------------
# 2. CLASS DIAGRAM
# -------------------------------------------------------------
def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(12, 9), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    def draw_class(x, y, w, h, name, attrs, methods, header_bg='#1E3A8A'):
        # Outer box
        box = patches.Rectangle((x, y), w, h, facecolor='#FFFFFF', edgecolor='#0F172A', linewidth=1.5)
        ax.add_patch(box)
        # Header box
        header_h = h * 0.22
        header_box = patches.Rectangle((x, y + h - header_h), w, header_h,
                                       facecolor=header_bg, edgecolor='#0F172A', linewidth=1.5)
        ax.add_patch(header_box)
        ax.text(x + w / 2, y + h - header_h / 2, name, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='#FFFFFF')

        # Attributes section
        attr_h = (h - header_h) * 0.45
        ax.plot([x, x + w], [y + h - header_h - attr_h, y + h - header_h - attr_h], color='#0F172A', lw=1)
        ax.text(x + 1.2, y + h - header_h - 1.5, "\n".join(attrs), ha='left', va='top',
                fontsize=6.8, fontfamily='monospace', color='#1E293B', linespacing=1.2)

        # Methods section
        ax.text(x + 1.2, y + h - header_h - attr_h - 1.5, "\n".join(methods), ha='left', va='top',
                fontsize=6.8, fontfamily='monospace', color='#0F172A', linespacing=1.2)

    # Class 1: User
    draw_class(4, 68, 26, 27, "User (Django Auth)",
               ["- id: Integer [PK]", "- username: String", "- email: String", "- password_hash: String", "- date_joined: DateTime"],
               ["+ register(): Boolean", "+ login(): Token", "+ reset_password(): Void", "+ authenticate(): User"],
               header_bg='#1E3A8A')

    # Class 2: UserProfile
    draw_class(37, 68, 27, 27, "UserProfile",
               ["- student_id: String", "- device_name: String", "- device_type: Enum", "- daily_goal_min: Int"],
               ["+ update_device(): Void", "+ set_screen_limit(): Void", "+ get_credentials(): Dict"],
               header_bg='#0284C7')

    # Class 3: VerificationCheck
    draw_class(71, 68, 26, 27, "VerificationCheck",
               ["- id: Integer [PK]", "- content: Text", "- source_url: URL", "- verdict: Enum", "- confidence: Float", "- explanation: Text"],
               ["+ analyze_claim(): Dict", "+ compute_confidence(): Float", "+ export_verdict(): JSON"],
               header_bg='#D97706')

    # Class 4: NLPEngine
    draw_class(71, 36, 26, 26, "NLPEngine",
               ["- vectorizer: TFIDF", "- classifier: MNB", "- gemini_api_key: String"],
               ["+ extract_features(): Vector", "+ query_gemini_ai(): Dict", "+ verify_news(): Dict"],
               header_bg='#B45309')

    # Class 5: ScreenTimeRecord
    draw_class(4, 36, 26, 26, "ScreenTimeRecord",
               ["- id: Integer [PK]", "- date: Date", "- total_screen_min: Int", "- unlock_count: Int", "- longest_session: Int", "- productivity_score: Int"],
               ["+ calculate_score(): Int", "+ get_daily_average(): Float", "+ sync_metrics(): Boolean"],
               header_bg='#047857')

    # Class 6: AppUsageRecord
    draw_class(37, 36, 27, 26, "AppUsageRecord",
               ["- app_name: String", "- category: Enum", "- usage_minutes: Int", "- open_count: Int", "- cpu_seconds: Float", "- memory_mb: Float"],
               ["+ log_foreground(): Void", "+ calculate_share(): Float", "+ categorize_app(): Enum"],
               header_bg='#059669')

    # Class 7: LaptopMonitor (Win32 OS)
    draw_class(4, 4, 26, 26, "LaptopMonitor",
               ["- boot_time: DateTime", "- idle_seconds: Float", "- battery_pct: Int", "- ram_used_gb: Float"],
               ["+ get_uptime(): Int", "+ get_idle_duration(): Float", "+ detect_running_apps(): List"],
               header_bg='#0F766E')

    # Class 8: RecommendationEngine
    draw_class(37, 4, 27, 26, "RecommendationEngine",
               ["- id: Integer [PK]", "- title: String", "- advice: Text", "- category: Enum", "- priority: Enum", "- is_completed: Boolean"],
               ["+ synthesize_habits(): List", "+ toggle_completion(): Void", "+ evaluate_eye_strain(): Bool"],
               header_bg='#6D28D9')

    # Class 9: LookerStudioAnalytics
    draw_class(71, 4, 26, 26, "AnalyticsOverview",
               ["- total_checks: Int", "- accuracy_rate: Float", "- category_counts: Dict", "- status_flags: Dict"],
               ["+ aggregate_metrics(): Dict", "+ export_looker_json(): JSON", "+ get_verdict_ratio(): Dict"],
               header_bg='#4338CA')

    # Relationships Lines
    # User -> UserProfile (1 to 1)
    ax.annotate("1", xy=(30, 82), xytext=(30.5, 82), fontsize=8, fontweight='bold', color='#1E3A8A')
    ax.annotate("1", xy=(36, 82), xytext=(35, 82), fontsize=8, fontweight='bold', color='#1E3A8A')
    ax.plot([30, 37], [81.5, 81.5], color='#1E3A8A', lw=1.5)

    # User -> VerificationCheck (1 to *)
    ax.plot([37 + 27, 71], [81.5, 81.5], color='#D97706', lw=1.5)
    ax.annotate("1", xy=(64.5, 83), fontsize=8, fontweight='bold', color='#D97706')
    ax.annotate("*", xy=(70, 83), fontsize=9, fontweight='bold', color='#D97706')

    # VerificationCheck -> NLPEngine (Dependency)
    ax.plot([84, 84], [68, 62], color='#D97706', lw=1.5, linestyle="--")
    ax.annotate("«uses»", xy=(84.5, 65), fontsize=7.5, color='#B45309', fontweight='bold')

    # User -> ScreenTimeRecord (1 to *)
    ax.plot([17, 17], [68, 62], color='#047857', lw=1.5)
    ax.annotate("1", xy=(18, 66), fontsize=8, fontweight='bold', color='#047857')
    ax.annotate("*", xy=(18, 63), fontsize=9, fontweight='bold', color='#047857')

    # ScreenTimeRecord -> AppUsageRecord (1 to * Composition)
    ax.plot([30, 37], [49, 49], color='#059669', lw=1.5)
    ax.scatter([30.5], [49], marker='D', color='#059669', s=30)
    ax.annotate("1", xy=(31.5, 50), fontsize=8, fontweight='bold')
    ax.annotate("*", xy=(35.5, 50), fontsize=9, fontweight='bold')

    # ScreenTimeRecord -> LaptopMonitor
    ax.plot([17, 17], [36, 30], color='#0F766E', lw=1.5)

    # ScreenTimeRecord -> RecommendationEngine
    ax.plot([30, 37], [17, 17], color='#6D28D9', lw=1.5, linestyle="--")
    ax.annotate("«triggers»", xy=(31, 18.5), fontsize=7, color='#6D28D9', fontweight='bold')

    # VerificationCheck -> AnalyticsOverview
    ax.plot([84, 84], [36, 30], color='#4338CA', lw=1.5)

    plt.tight_layout()
    plt.savefig('scratch/uml_diagrams/02_class_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

# -------------------------------------------------------------
# 3. SEQUENCE DIAGRAM
# -------------------------------------------------------------
def generate_sequence_diagram():
    fig, ax = plt.subplots(figsize=(12, 9), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Lifelines
    lifelines = [
        ("User (Client)", 10, '#38BDF8'),
        ("React Frontend", 28, '#0284C7'),
        ("Django REST API", 48, '#1E3A8A'),
        ("NLP / Scikit Engine", 66, '#D97706'),
        ("Google Gemini API", 82, '#DC2626'),
        ("MySQL Database", 94, '#059669')
    ]

    for name, x, color in lifelines:
        # Box header
        rect = patches.FancyBboxPatch((x - 6.5, 92), 13, 5, boxstyle="round,pad=0.3",
                                      facecolor=color, edgecolor='#0F172A', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, 94.5, name, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#FFFFFF')
        # Dashed lifeline
        ax.plot([x, x], [92, 6], color='#64748B', lw=1.2, linestyle="--")

    # Message arrows
    messages = [
        (10, 28, 86, "1. Enter Claim Text & Click 'Verify Claim'", False),
        (28, 48, 80, "2. POST /api/verify/ {content, url}", False),
        (48, 66, 74, "3. extract_features() & tokenize text", False),
        (66, 48, 68, "4. Return heuristic lexical signal vector", True),
        (48, 82, 62, "5. generateContent(claim, context)", False),
        (82, 48, 54, "6. Structured Verdict, Score & Citations", True),
        (48, 94, 46, "7. INSERT INTO VerificationCheck", False),
        (94, 48, 40, "8. DB Confirmation (ID, Timestamp)", True),
        (48, 28, 32, "9. JSON Response {verdict, confidence, citations}", True),
        (28, 10, 24, "10. Render Live Glowing Badge & Evidence Summary", True),
        (28, 48, 16, "11. POST /api/wellbeing/session (Update Active Time)", False),
        (48, 94, 10, "12. Log ScreenTime & Productivity Metrics", False)
    ]

    # Activation boxes
    activations = [
        (10, 86, 24),
        (28, 86, 16),
        (48, 80, 10),
        (66, 74, 68),
        (82, 62, 54),
        (94, 46, 40),
        (94, 10, 6)
    ]

    for lx, y_top, y_bot in activations:
        act_box = patches.Rectangle((lx - 1, y_bot), 2, y_top - y_bot,
                                    facecolor='#CBD5E1', edgecolor='#334155', linewidth=1)
        ax.add_patch(act_box)

    for x1, x2, y, label, is_return in messages:
        style = "<--" if (is_return and x1 < x2) else ("-->" if is_return else "->")
        line_style = "--" if is_return else "-"
        color = '#0284C7' if not is_return else '#059669'

        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.3, linestyle=line_style))

        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 1.2, label, ha='center', va='bottom',
                fontsize=7.2, fontweight='medium', color='#0F172A',
                bbox=dict(boxstyle="square,pad=0.1", fc="#FFFFFF", ec="none", alpha=0.85))

    plt.tight_layout()
    plt.savefig('scratch/uml_diagrams/03_sequence_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

# -------------------------------------------------------------
# 4. ACTIVITY DIAGRAM
# -------------------------------------------------------------
def generate_activity_diagram():
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Initial Node
    start = patches.Circle((50, 96), 2, facecolor='#0F172A', edgecolor='#0F172A')
    ax.add_patch(start)
    ax.annotate("", xy=(50, 90), xytext=(50, 94), arrowprops=dict(arrowstyle="->", lw=1.5, color='#0F172A'))

    def draw_action(cx, cy, w, h, text, bg='#E0F2FE', border='#0284C7'):
        rect = patches.FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0.8",
                                      facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=7.5, fontweight='semibold', color='#0F172A')

    def draw_decision(cx, cy, w, h, label):
        pts = [[cx, cy + h / 2], [cx + w / 2, cy], [cx, cy - h / 2], [cx - w / 2, cy]]
        poly = patches.Polygon(pts, closed=True, facecolor='#FEF3C7', edgecolor='#D97706', linewidth=1.5)
        ax.add_patch(poly)
        ax.text(cx, cy, label, ha='center', va='center', fontsize=7, fontweight='bold', color='#78350F')

    # 1. Action: Receive Input
    draw_action(50, 87, 40, 5, "Receive Claim Text / URL Input")
    ax.annotate("", xy=(50, 79), xytext=(50, 84.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='#0F172A'))

    # 2. Decision: Validate Input
    draw_decision(50, 75, 24, 7, "Is Input Valid?")
    # No branch
    ax.plot([62, 78, 78], [75, 75, 87], color='#DC2626', lw=1.3)
    ax.annotate("", xy=(70, 87), xytext=(78, 87), arrowprops=dict(arrowstyle="->", lw=1.3, color='#DC2626'))
    ax.text(68, 76.5, "[No: Empty]", fontsize=6.8, color='#DC2626', fontweight='bold')
    draw_action(84, 87, 16, 4.5, "Show Error Prompt", bg='#FEE2E2', border='#DC2626')
    # Yes branch
    ax.annotate("", xy=(50, 67), xytext=(50, 71.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='#0F172A'))
    ax.text(51.5, 69, "[Yes]", fontsize=6.8, color='#047857', fontweight='bold')

    # 3. Action: Parallel Fork
    draw_action(50, 64, 46, 5, "Tokenization & Lexical Feature Extraction")
    ax.annotate("", xy=(50, 58), xytext=(50, 61.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='#0F172A'))

    # Fork Bar
    fork1 = patches.Rectangle((20, 57.5), 60, 1.2, facecolor='#0F172A')
    ax.add_patch(fork1)

    # Parallel branches
    ax.annotate("", xy=(30, 52), xytext=(30, 57.5), arrowprops=dict(arrowstyle="->", lw=1.3))
    draw_action(30, 48, 30, 6.5, "Execute TF-IDF Matrix\n& Heuristic Scoring")

    ax.annotate("", xy=(70, 52), xytext=(70, 57.5), arrowprops=dict(arrowstyle="->", lw=1.3))
    draw_action(70, 48, 32, 6.5, "Query Google Gemini AI API\n(Grounded Fact Verification)")

    # Join Bar
    ax.annotate("", xy=(30, 40), xytext=(30, 44.5), arrowprops=dict(arrowstyle="->", lw=1.3))
    ax.annotate("", xy=(70, 40), xytext=(70, 44.5), arrowprops=dict(arrowstyle="->", lw=1.3))
    join1 = patches.Rectangle((20, 39), 60, 1.2, facecolor='#0F172A')
    ax.add_patch(join1)

    # 4. Synthesize Verdict & Citations
    ax.annotate("", xy=(50, 34), xytext=(50, 39), arrowprops=dict(arrowstyle="->", lw=1.5, color='#0F172A'))
    draw_action(50, 31, 46, 5.5, "Fuse Multi-Modal Verdict, Confidence & Citations", bg='#FEF3C7', border='#D97706')

    # 5. Persist to DB & Read OS Screen Time
    ax.annotate("", xy=(50, 24), xytext=(50, 28), arrowprops=dict(arrowstyle="->", lw=1.5, color='#0F172A'))
    draw_action(50, 21, 50, 5.5, "Persist Record in MySQL & Sample Win32 Uptime", bg='#DCFCE7', border='#16A34A')

    # 6. Recommendation Trigger Decision
    ax.annotate("", xy=(50, 14.5), xytext=(50, 18), arrowprops=dict(arrowstyle="->", lw=1.5, color='#0F172A'))
    draw_decision(50, 12, 28, 6.5, "Session > 45m?")

    # Yes branch -> Recommend Break
    ax.annotate("", xy=(78, 12), xytext=(64, 12), arrowprops=dict(arrowstyle="->", lw=1.3, color='#B45309'))
    ax.text(67, 13.5, "[Yes]", fontsize=6.8, color='#B45309', fontweight='bold')
    draw_action(88, 12, 18, 5, "Trigger 20-20-20\nBreak Notification", bg='#F3E8FF', border='#7E22CE')

    # No branch -> Display Dashboard
    ax.annotate("", xy=(50, 5.5), xytext=(50, 8.8), arrowprops=dict(arrowstyle="->", lw=1.5, color='#0F172A'))
    ax.text(51.5, 7.2, "[No]", fontsize=6.8, color='#047857', fontweight='bold')
    ax.plot([88, 88, 50], [9.5, 2.5, 2.5], color='#7E22CE', lw=1.2)

    # Final Node
    end_outer = patches.Circle((50, 2.5), 2.2, facecolor='#FFFFFF', edgecolor='#0F172A', linewidth=1.5)
    end_inner = patches.Circle((50, 2.5), 1.3, facecolor='#0F172A', edgecolor='#0F172A')
    ax.add_patch(end_outer)
    ax.add_patch(end_inner)

    plt.tight_layout()
    plt.savefig('scratch/uml_diagrams/04_activity_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

# -------------------------------------------------------------
# 5. STATE MACHINE DIAGRAM
# -------------------------------------------------------------
def generate_state_diagram():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8.5), dpi=300)
    for ax in [ax1, ax2]:
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Sub-diagram 1: Claim Lifecycle
    ax1.text(50, 95, "SUB-DIAGRAM A: CLAIM VERIFICATION STATE MACHINE", ha='center', va='center',
             fontsize=10.5, fontweight='bold', color='#1E3A8A')

    # Initial
    s1 = patches.Circle((8, 60), 2.2, facecolor='#0F172A')
    ax1.add_patch(s1)

    def draw_state(ax, cx, cy, w, h, name, desc="", bg='#E0F2FE', border='#0284C7'):
        rect = patches.FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=1.2",
                                      facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect)
        if desc:
            ax.text(cx, cy + 2, name, ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')
            ax.text(cx, cy - 3, desc, ha='center', va='center', fontsize=6.5, color='#475569')
        else:
            ax.text(cx, cy, name, ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')

    # States
    draw_state(ax1, 22, 60, 18, 14, "Submitted", "Input Captured")
    draw_state(ax1, 44, 60, 18, 14, "Processing", "NLP & Tokenize")
    draw_state(ax1, 68, 60, 20, 14, "Evaluating", "Gemini AI Query")
    draw_state(ax1, 90, 60, 16, 14, "Verdicted", "True/False/Misc", bg='#FEF3C7', border='#D97706')

    # Transitions
    ax1.annotate("", xy=(13, 60), xytext=(10, 60), arrowprops=dict(arrowstyle="->", lw=1.3))
    ax1.annotate("", xy=(35, 60), xytext=(31, 60), arrowprops=dict(arrowstyle="->", lw=1.3))
    ax1.text(33, 63, "validate()", ha='center', fontsize=6.8, color='#1E293B')

    ax1.annotate("", xy=(58, 60), xytext=(53, 60), arrowprops=dict(arrowstyle="->", lw=1.3))
    ax1.text(55.5, 63, "extract()", ha='center', fontsize=6.8, color='#1E293B')

    ax1.annotate("", xy=(82, 60), xytext=(78, 60), arrowprops=dict(arrowstyle="->", lw=1.3))
    ax1.text(80, 63, "fuse_scores()", ha='center', fontsize=6.8, color='#1E293B')

    # Archived / Final State
    draw_state(ax1, 68, 20, 22, 12, "Archived / Indexed", "Stored in MySQL", bg='#DCFCE7', border='#16A34A')
    ax1.annotate("", xy=(79, 20), xytext=(90, 53), arrowprops=dict(arrowstyle="->", lw=1.3, color='#047857'))
    ax1.text(88, 35, "persist_check()", fontsize=6.8, color='#047857')

    end_out1 = patches.Circle((46, 20), 2.4, facecolor='#FFFFFF', edgecolor='#0F172A', linewidth=1.5)
    end_in1 = patches.Circle((46, 20), 1.4, facecolor='#0F172A')
    ax1.add_patch(end_out1)
    ax1.add_patch(end_in1)
    ax1.annotate("", xy=(48.5, 20), xytext=(57, 20), arrowprops=dict(arrowstyle="->", lw=1.3))

    # Sub-diagram 2: Digital Wellbeing States
    ax2.text(50, 95, "SUB-DIAGRAM B: DIGITAL WELLBEING & SCREEN TIME STATE MACHINE", ha='center', va='center',
             fontsize=10.5, fontweight='bold', color='#047857')

    s2 = patches.Circle((8, 55), 2.2, facecolor='#0F172A')
    ax2.add_patch(s2)

    draw_state(ax2, 22, 55, 18, 14, "System Booted", "Uptime Timer=0", bg='#DCFCE7', border='#16A34A')
    draw_state(ax2, 46, 55, 20, 14, "Active Focused", "User typing / mouse", bg='#E0F2FE', border='#0284C7')
    draw_state(ax2, 46, 18, 20, 14, "Idle / Paused", "GetLastInput > 180s", bg='#F1F5F9', border='#64748B')
    draw_state(ax2, 76, 55, 22, 14, "Extended Strain", "Session > 45 mins", bg='#FEE2E2', border='#DC2626')
    draw_state(ax2, 76, 18, 22, 14, "Break Restored", "20-20-20 Followed", bg='#F3E8FF', border='#7E22CE')

    # Transitions
    ax2.annotate("", xy=(13, 55), xytext=(10, 55), arrowprops=dict(arrowstyle="->", lw=1.3))
    ax2.annotate("", xy=(36, 55), xytext=(31, 55), arrowprops=dict(arrowstyle="->", lw=1.3))

    # Active <-> Idle
    ax2.annotate("", xy=(43, 25), xytext=(43, 48), arrowprops=dict(arrowstyle="->", lw=1.3, color='#64748B'))
    ax2.text(37, 36, "idle > 3m", fontsize=6.5, color='#64748B')
    ax2.annotate("", xy=(49, 48), xytext=(49, 25), arrowprops=dict(arrowstyle="->", lw=1.3, color='#0284C7'))
    ax2.text(51, 36, "user_input()", fontsize=6.5, color='#0284C7')

    # Active -> Extended Strain
    ax2.annotate("", xy=(65, 55), xytext=(56, 55), arrowprops=dict(arrowstyle="->", lw=1.3, color='#DC2626'))
    ax2.text(60.5, 58, "timer > 45m", fontsize=6.8, color='#DC2626')

    # Extended Strain -> Break Restored
    ax2.annotate("", xy=(76, 25), xytext=(76, 48), arrowprops=dict(arrowstyle="->", lw=1.3, color='#7E22CE'))
    ax2.text(78, 36, "adopt_habit()", fontsize=6.8, color='#7E22CE')

    # Break Restored -> Active
    ax2.annotate("", xy=(56, 49), xytext=(65, 24), arrowprops=dict(arrowstyle="->", lw=1.3, color='#047857'))
    ax2.text(61, 30, "resume_work()", fontsize=6.8, color='#047857')

    plt.tight_layout()
    plt.savefig('scratch/uml_diagrams/05_state_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

# -------------------------------------------------------------
# 6. PACKAGE DIAGRAM
# -------------------------------------------------------------
def generate_package_diagram():
    fig, ax = plt.subplots(figsize=(11, 8.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    def draw_package(x, y, w, h, name, contents, bg='#F8FAFC', border='#1E3A8A'):
        # Tab
        tab_w = w * 0.35
        tab_h = h * 0.16
        tab = patches.Rectangle((x, y + h), tab_w, tab_h, facecolor=border, edgecolor=border)
        ax.add_patch(tab)
        ax.text(x + tab_w / 2, y + h + tab_h / 2, name[:12], ha='center', va='center',
                fontsize=7, fontweight='bold', color='#FFFFFF')

        # Main Body
        box = patches.Rectangle((x, y), w, h, facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(box)
        ax.text(x + w / 2, y + h - 3, name, ha='center', va='top',
                fontsize=8.5, fontweight='bold', color=border)

        # Content List
        ax.text(x + 2, y + h - 8, "\n".join(contents), ha='left', va='top',
                fontsize=7, color='#1E293B', linespacing=1.3)

    # 1. Presentation Package (Next.js)
    draw_package(6, 68, 40, 26, "com.veracity.presentation (Next.js)",
                 ["+ RumoursFeed.jsx (Claims Stream)",
                  "+ QuickCheck.jsx (Instant Claim Verify)",
                  "+ VerifierChat.jsx (AI Assistant)",
                  "+ WellbeingDashboard.jsx (Screen Time)",
                  "+ CyberGlobe3D.jsx (3D Canvas)",
                  "+ LookerEmbedView.jsx (Visualizations)"],
                 bg='#EFF6FF', border='#1D4ED8')

    # 2. REST API Controller Package (Django)
    draw_package(54, 68, 40, 26, "com.veracity.api_controllers (Django DRF)",
                 ["+ auth_views.py (Register / Login / Profile)",
                  "+ verification_views.py (Claim Verify & History)",
                  "+ chatbot_views.py (Conversational Bot)",
                  "+ wellbeing_views.py (Summary & Telemetry)",
                  "+ recommendations_views.py (Habit Engine)",
                  "+ analytics_views.py (Looker Overview)"],
                 bg='#F0FDF4', border='#047857')

    # 3. AI & NLP Engine Package
    draw_package(6, 36, 40, 26, "com.veracity.ai_intelligence",
                 ["+ GeminiClient (Google Generative AI)",
                  "+ ScikitClassifier (TF-IDF Vectorizer + MNB)",
                  "+ NLTKFeatureExtractor (Linguistic Signals)",
                  "+ URLCredibilityEvaluator (Journalistic Whitelist)",
                  "+ HabitSynthesizer (AI Screen Health)"],
                 bg='#FFFBEB', border='#B45309')

    # 4. Hardware & Telemetry Package
    draw_package(54, 36, 40, 26, "com.veracity.telemetry",
                 ["+ LaptopMonitor (Win32 kernel32/user32)",
                  "+ ProcessScanner (psutil Active Process List)",
                  "+ UserActivityDetector (GetLastInputInfo)",
                  "+ HardwareSensors (Battery, RAM, CPU %)",
                  "+ AndroidBridge (UsageStatsManager Ingestion)"],
                 bg='#FAF5FF', border='#7E22CE')

    # 5. Data Access & Models Package
    draw_package(30, 4, 40, 25, "com.veracity.data_persistence (MySQL / ORM)",
                 ["+ User & UserProfile Models",
                  "+ VerificationCheck Model",
                  "+ ScreenTimeRecord Model",
                  "+ AppUsageRecord Model",
                  "+ DigitalHabitRecommendation Model",
                  "+ Django ORM Migration Engine"],
                 bg='#F8FAFC', border='#0F172A')

    # Package Dependency Arrows
    # Presentation -> API Controllers
    ax.annotate("«http/json»", xy=(54, 81), xytext=(46, 81),
                arrowprops=dict(arrowstyle="->", color='#1D4ED8', lw=1.5, linestyle="--"),
                ha='center', va='bottom', fontsize=7, fontweight='bold', color='#1D4ED8')

    # API Controllers -> AI Intelligence
    ax.annotate("«invokes»", xy=(46, 54), xytext=(54, 68),
                arrowprops=dict(arrowstyle="->", color='#047857', lw=1.5, linestyle="--"),
                fontsize=7, fontweight='bold', color='#047857')

    # API Controllers -> Telemetry
    ax.annotate("«reads»", xy=(74, 62), xytext=(74, 68),
                arrowprops=dict(arrowstyle="->", color='#047857', lw=1.5, linestyle="--"),
                fontsize=7, fontweight='bold', color='#047857')

    # API Controllers & AI & Telemetry -> Data Persistence
    ax.annotate("", xy=(50, 29), xytext=(65, 36), arrowprops=dict(arrowstyle="->", color='#0F172A', lw=1.3, linestyle="--"))
    ax.annotate("", xy=(50, 29), xytext=(35, 36), arrowprops=dict(arrowstyle="->", color='#0F172A', lw=1.3, linestyle="--"))

    plt.tight_layout()
    plt.savefig('scratch/uml_diagrams/06_package_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

# -------------------------------------------------------------
# 7. DEPLOYMENT & COMPONENT DIAGRAM
# -------------------------------------------------------------
def generate_deployment_diagram():
    fig, ax = plt.subplots(figsize=(11, 8.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    def draw_node(x, y, w, h, name, desc="", bg='#F8FAFC', border='#1E3A8A'):
        # 3D Node box effect
        depth = 2.5
        front = patches.Rectangle((x, y), w, h, facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(front)
        # Top flap
        top_pts = [[x, y + h], [x + depth, y + h + depth], [x + w + depth, y + h + depth], [x + w, y + h]]
        ax.add_patch(patches.Polygon(top_pts, closed=True, facecolor='#E2E8F0', edgecolor=border, lw=1.5))
        # Right flap
        right_pts = [[x + w, y], [x + w + depth, y + depth], [x + w + depth, y + h + depth], [x + w, y + h]]
        ax.add_patch(patches.Polygon(right_pts, closed=True, facecolor='#CBD5E1', edgecolor=border, lw=1.5))

        ax.text(x + w / 2, y + h - 3, name, ha='center', va='top', fontsize=8.5, fontweight='bold', color=border)
        if desc:
            ax.text(x + w / 2, y + h - 6.5, desc, ha='center', va='top', fontsize=7, color='#64748B')

    def draw_artifact(x, y, w, h, title, items):
        box = patches.Rectangle((x, y), w, h, facecolor='#FFFFFF', edgecolor='#475569', linewidth=1.2)
        ax.add_patch(box)
        ax.text(x + w / 2, y + h - 2.5, f"«artifact»\n{title}", ha='center', va='top',
                fontsize=7, fontweight='bold', color='#0F172A')
        ax.text(x + 1.5, y + h - 8, "\n".join(items), ha='left', va='top',
                fontsize=6.2, color='#334155', linespacing=1.2)

    # Node 1: Client Machine
    draw_node(5, 52, 28, 42, "«device»\nClient Workstation", "Windows 11 / AMD64 Laptop", bg='#EFF6FF', border='#1D4ED8')
    draw_artifact(7, 54, 24, 28, "Web Browser (Chrome/Edge)",
                  ["* React 19 Frontend App",
                   "* CyberGlobe3D Canvas",
                   "* LocalStorage Token Cache",
                   "* HTML5 Visibility API"])

    # Node 2: Web Server (Node.js)
    draw_node(38, 52, 26, 42, "«execution environment»\nNext.js Application Server", "Node.js 18+ (Port 3000)", bg='#F0FDF4', border='#047857')
    draw_artifact(40, 54, 22, 28, "Next.js Webpack Build",
                  ["* Server-Side Rendering (SSR)",
                   "* Static Page Router (23 routes)",
                   "* Tailwind CSS 4 Styling",
                   "* Client-Side Query Hydration"])

    # Node 3: Backend Application Server (Django)
    draw_node(69, 52, 28, 42, "«execution environment»\nDjango REST Backend Server", "Python 3.14 (Port 8000)", bg='#FFFBEB', border='#B45309')
    draw_artifact(71, 54, 24, 28, "Django WSGI / REST App",
                  ["* Authentication & JWT Layer",
                   "* Scikit-Learn TFIDF Engine",
                   "* Win32 OS Telemetry Agent",
                   "* Recommendation Synthesizer"])

    # Node 4: Database Server
    draw_node(38, 4, 26, 38, "«database system»\nRelational Database Engine", "MySQL / SQLite 3", bg='#F8FAFC', border='#0F172A')
    draw_artifact(40, 6, 22, 26, "veracity_ai_db",
                  ["* VerificationCheck Table",
                   "* User & Profile Records",
                   "* ScreenTimeDaily Table",
                   "* AppUsageMetrics Table"])

    # Node 5: Cloud AI API Service
    draw_node(69, 4, 28, 38, "«cloud service»\nGoogle Cloud Platform", "Gemini 1.5 API Services", bg='#FAF5FF', border='#7E22CE')
    draw_artifact(71, 6, 24, 26, "Gemini Generative API",
                  ["* LLM Grounded Verification",
                   "* Confidence Scoring Model",
                   "* Citation & Web Reasoning",
                   "* HTTPS / TLS 1.3 Endpoint"])

    # Connections
    # Client -> Next.js (HTTP/HTTPS)
    ax.annotate("", xy=(38, 73), xytext=(33, 73),
                arrowprops=dict(arrowstyle="<->", color='#1D4ED8', lw=1.8))
    ax.text(35.5, 75, "HTTP:3000", ha='center', fontsize=6.8, fontweight='bold', color='#1D4ED8')

    # Next.js -> Django (REST JSON)
    ax.annotate("", xy=(69, 73), xytext=(64, 73),
                arrowprops=dict(arrowstyle="<->", color='#047857', lw=1.8))
    ax.text(66.5, 75, "REST:8000", ha='center', fontsize=6.8, fontweight='bold', color='#047857')

    # Django -> Database (TCP 3306 / ORM)
    ax.annotate("", xy=(51, 42), xytext=(72, 52),
                arrowprops=dict(arrowstyle="<->", color='#0F172A', lw=1.6))
    ax.text(63, 44, "TCP/MySQL", fontsize=6.8, fontweight='bold', color='#0F172A')

    # Django -> Gemini (HTTPS:443)
    ax.annotate("", xy=(83, 42), xytext=(83, 52),
                arrowprops=dict(arrowstyle="<->", color='#7E22CE', lw=1.6))
    ax.text(85, 47, "HTTPS:443", fontsize=6.8, fontweight='bold', color='#7E22CE')

    plt.tight_layout()
    plt.savefig('scratch/uml_diagrams/07_component_deployment_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    print("Generating all 7 UML Design Diagrams...")
    generate_use_case()
    print("1/7: Use Case Diagram done")
    generate_class_diagram()
    print("2/7: Class Diagram done")
    generate_sequence_diagram()
    print("3/7: Sequence Diagram done")
    generate_activity_diagram()
    print("4/7: Activity Diagram done")
    generate_state_diagram()
    print("5/7: State Diagram done")
    generate_package_diagram()
    print("6/7: Package Diagram done")
    generate_deployment_diagram()
    print("7/7: Deployment Diagram done")
    print("All diagrams generated successfully!")
