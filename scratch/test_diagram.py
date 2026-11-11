import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('scratch/uml_diagrams', exist_ok=True)

def create_use_case_diagram():
    fig, ax = plt.subplots(figsize=(12, 9), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # System Boundary Box
    system_box = patches.FancyBboxPatch((24, 5), 52, 90, boxstyle="round,pad=1.5",
                                        facecolor='#F8FAFC', edgecolor='#1E3A8A', linewidth=2.5)
    ax.add_patch(system_box)
    ax.text(50, 92, "VERACITY AI PLATFORM (SYSTEM BOUNDARY)", ha='center', va='center',
            fontsize=13, fontweight='bold', color='#1E3A8A', fontfamily='sans-serif')

    # Actors
    def draw_actor(x, y, name, role):
        # Head
        head = patches.Circle((x, y + 4), 2.2, facecolor='#E2E8F0', edgecolor='#0F172A', linewidth=1.8)
        ax.add_patch(head)
        # Body
        ax.plot([x, x], [y + 1.8, y - 3.5], color='#0F172A', lw=2)
        # Arms
        ax.plot([x - 2.8, x + 2.8], [y + 0.2, y + 0.2], color='#0F172A', lw=2)
        # Legs
        ax.plot([x, x - 2.5], [y - 3.5, y - 7.5], color='#0F172A', lw=2)
        ax.plot([x, x + 2.5], [y - 3.5, y - 7.5], color='#0F172A', lw=2)
        # Label
        ax.text(x, y - 10, name, ha='center', va='top', fontsize=9.5, fontweight='bold', color='#0F172A')
        ax.text(x, y - 12.5, f"({role})", ha='center', va='top', fontsize=7.5, color='#475569')

    draw_actor(12, 70, "User / Student", "Primary Actor")
    draw_actor(12, 28, "Fact-Checker / Admin", "Secondary Actor")
    draw_actor(88, 70, "Google Gemini AI", "External AI Service")
    draw_actor(88, 28, "OS & Telemetry API", "Win32 / Android")

    # Use Cases (Ovals)
    use_cases = [
        ("UC1: User Authentication\n& Profile Management", 50, 84, '#E0F2FE', '#0284C7'),
        ("UC2: Submit News Claim\n& Text for Verification", 50, 72, '#E0F2FE', '#0284C7'),
        ("UC3: Submit URL for Domain\nCredibility Analysis", 50, 60, '#E0F2FE', '#0284C7'),
        ("UC4: Real-Time AI Fact-Checking\n& Confidence Scoring", 50, 48, '#FEF3C7', '#D97706'),
        ("UC5: Conversational Verification\nvia AI Chatbot", 50, 36, '#E0F2FE', '#0284C7'),
        ("UC6: Track Laptop Screen Time\n& Active Hardware Sensors", 50, 24, '#DCFCE7', '#16A34A'),
        ("UC7: View Digital Habits &\nAI Recommendations", 50, 12, '#DCFCE7', '#16A34A')
    ]

    for text, cx, cy, bg, border in use_cases:
        ellipse = patches.Ellipse((cx, cy), 28, 7.8, facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(ellipse)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=8, fontweight='semibold', color='#0F172A')

    # Association Lines
    # User to UC1, UC2, UC3, UC5, UC6, UC7
    user_pts = [(12, 68)]
    for target in [(36, 84), (36, 72), (36, 60), (36, 36), (36, 24), (36, 12)]:
        ax.annotate("", xy=target, xytext=(15, 68),
                    arrowprops=dict(arrowstyle="-", color='#334155', lw=1.2))

    # Admin to UC1, UC4, UC7
    for target in [(36, 84), (36, 48), (36, 12)]:
        ax.annotate("", xy=target, xytext=(15, 28),
                    arrowprops=dict(arrowstyle="-", color='#334155', lw=1.2))

    # Gemini to UC4, UC5, UC7
    for target in [(64, 48), (64, 36), (64, 12)]:
        ax.annotate("", xy=target, xytext=(85, 68),
                    arrowprops=dict(arrowstyle="-", color='#D97706', lw=1.3, linestyle="--"))

    # Telemetry API to UC6, UC7
    for target in [(64, 24), (64, 12)]:
        ax.annotate("", xy=target, xytext=(85, 28),
                    arrowprops=dict(arrowstyle="-", color='#16A34A', lw=1.3, linestyle="--"))

    # Include relationships: UC2 -> UC4 and UC3 -> UC4
    ax.annotate("«include»", xy=(50, 52), xytext=(50, 68),
                arrowprops=dict(arrowstyle="->", color='#0284C7', lw=1.2, linestyle=":"),
                ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0284C7')

    plt.tight_layout()
    plt.savefig('scratch/uml_diagrams/01_use_case_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Use Case Diagram created successfully!")

if __name__ == '__main__':
    create_use_case_diagram()
