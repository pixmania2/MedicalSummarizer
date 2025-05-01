
"""
Convert synthetic_medical_reports.jsonl → nicely-formatted PDFs.

Each PDF contains:
  • Title (“Medical Report #00001”)
  • Abstractive Summary (one-liner)
  • The full long-form report, with headings and bullets preserved
"""

import os, json
from reportlab.lib.pagesizes import letter
from reportlab.lib.units   import inch
from reportlab.platypus    import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles  import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums   import TA_CENTER, TA_LEFT

# ————————————————————————
JSONL_FILE  = "synthetic_medical_reports.jsonl"      # <— update if needed
OUTPUT_DIR  = "pdf_reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ————————————————————————
# build a style sheet (avoid duplicate names)
styles = getSampleStyleSheet()

def safe_add(name, **kwargs):
    """Only add a ParagraphStyle if it’s not already defined."""
    if name not in styles:
        styles.add(ParagraphStyle(name=name, **kwargs))

safe_add(
    "ReportTitle",
    parent=styles["Heading1"],
    fontSize=18, alignment=TA_CENTER,
    spaceAfter=12,
)
safe_add(
    "SectionHeader",
    parent=styles["Heading2"],
    fontSize=12, alignment=TA_LEFT,
    spaceAfter=6,
)
safe_add(
    "ReportBody",
    parent=styles["BodyText"],
    fontSize=10, leading=12,
    leftIndent=0, spaceAfter=4,
)
safe_add(
    "BulletText",
    parent=styles["BodyText"],
    fontSize=10, leading=12,
    leftIndent=12, spaceAfter=4,
)
safe_add(
    "SummaryText",                       # ★ NEW
    parent=styles["Italic"],
    fontSize=11, leading=13,
    leftIndent=0, spaceAfter=10,
)

# ————————————————————————
def build_story(record, idx):
    """Return a Platypus story (list of flowables) for one report."""
    story = []

    # Title
    story.append(Paragraph(f"Medical Report #{idx:05d}", styles["ReportTitle"]))
    story.append(Spacer(1, 0.15 * inch))

    # Summary panel
    if "summary" in record:
        story.append(Paragraph("ABSTRACTIVE SUMMARY:", styles["SectionHeader"]))
        story.append(Paragraph(record["summary"], styles["SummaryText"]))
        story.append(Spacer(1, 0.1 * inch))

    # Full report text — preserve headings / bullets
    for raw in record["report_text"].splitlines():
        line = raw.strip()
        if not line:
            story.append(Spacer(1, 0.08 * inch))
            continue

        if line.endswith(":") and line == line.upper():
            story.append(Paragraph(line, styles["SectionHeader"]))
        elif line.startswith("- "):
            story.append(Paragraph(line, styles["BulletText"]))
        else:
            story.append(Paragraph(line, styles["ReportBody"]))

    return story

# ————————————————————————
def main():
    with open(JSONL_FILE, "r", encoding="utf-8") as infile:
        for idx, line in enumerate(infile, start=1):
            record = json.loads(line)

            pdf_path = os.path.join(OUTPUT_DIR, f"report_{idx:05d}.pdf")
            doc = SimpleDocTemplate(
                pdf_path,
                pagesize=letter,
                rightMargin=0.75 * inch,
                leftMargin=0.75 * inch,
                topMargin=0.75 * inch,
                bottomMargin=0.75 * inch,
            )

            story = build_story(record, idx)
            doc.build(story)

    print(f"Generated PDFs for {idx} reports → '{OUTPUT_DIR}/'")

# ————————————————————————
if __name__ == "__main__":
    main()
