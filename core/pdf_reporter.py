from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime
import os
import re

DARK = HexColor('#0d1117')
TEAL = HexColor('#00d4aa')
LIGHT_BG = HexColor('#f4f5f7')
MEDIUM_GRAY = HexColor('#6b7280')
RED = HexColor('#ef4444')
ORANGE = HexColor('#f59e0b')
GREEN = HexColor('#10b981')
DARKRED = HexColor('#7f1d1d')

def get_risk_color(label):
    if label == "LOW RISK": return GREEN
    elif label == "MEDIUM RISK": return ORANGE
    elif label == "HIGH RISK": return RED
    else: return DARKRED

def extract_section(text, section_name):
    pattern = rf'{section_name}:\s*\n(.*?)(?=\n[A-Z\s]+:|$)'
    match = re.search(pattern, text, re.DOTALL)
    if not match: return []
    block = match.group(1)
    items = re.findall(r'-\s(.+)', block)
    return [item.strip() for item in items if item.strip()]

def generate_pdf_report(scored_results: dict, overall: dict, company_name: str) -> str:
    os.makedirs("outputs/reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = company_name.replace(" ", "_").lower()
    filename = f"outputs/reports/{safe_name}_{timestamp}.pdf"

    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        rightMargin=20*mm, leftMargin=20*mm,
        topMargin=20*mm, bottomMargin=20*mm
    )

    story = []

    # Header
    header_data = [[
        Paragraph(
            '<b>AUDITX</b><br/>'
            '<font size="8">AI-POWERED GRC COMPLIANCE PLATFORM</font>',
            ParagraphStyle('h', fontSize=22, fontName='Helvetica-Bold',
                          textColor=TEAL, leading=28)
        ),
        Paragraph(
            '<font size="8">BYTEFORTIX SECURITY<br/>'
            'kaifhoda1@gmail.com<br/>'
            'github.com/kaifhoda1</font>',
            ParagraphStyle('r', fontSize=8, alignment=TA_RIGHT,
                          textColor=MEDIUM_GRAY, leading=14)
        )
    ]]
    header_table = Table(header_data, colWidths=[110*mm, 60*mm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6*mm))

    # Client info
    now = datetime.now().strftime("%B %d, %Y  %H:%M")
    info_data = [
        ['Company', company_name, 'Generated', now],
        ['Overall Score', f"{overall['score']}/100", 'Risk Level', overall['label']],
        ['Frameworks', str(len(scored_results)), 'Status', 'DRAFT — Awaiting Auditor Review'],
    ]
    info_table = Table(info_data, colWidths=[35*mm, 65*mm, 35*mm, 35*mm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), LIGHT_BG),
        ('BACKGROUND', (2,0), (2,-1), LIGHT_BG),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#e5e7eb')),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 6*mm))

    # Score summary
    story.append(Paragraph('COMPLIANCE SCORES',
        ParagraphStyle('sec', fontSize=10, fontName='Helvetica-Bold',
                      textColor=DARK, spaceAfter=4)))
    story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=4))

    score_rows = [['Framework', 'Score', 'Risk Level', 'Result']]
    score_rows.append(['OVERALL', f"{overall['score']}/100", overall['label'], '---'])
    for fw, result in scored_results.items():
        score_rows.append([
            result.get('framework_name', fw),
            f"{result.get('score', 0)}/100",
            result.get('label', 'UNKNOWN'),
            'PASS' if result.get('score', 0) >= 60 else 'FAIL'
        ])

    score_table = Table(score_rows, colWidths=[80*mm, 25*mm, 40*mm, 25*mm])
    table_style = [
        ('BACKGROUND', (0,0), (-1,0), DARK),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#e5e7eb')),
        ('BACKGROUND', (0,1), (-1,1), HexColor('#f0fdf4')),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
    ]
    for i, (fw, result) in enumerate(scored_results.items(), 2):
        color = get_risk_color(result.get('label', ''))
        table_style.append(('TEXTCOLOR', (2,i), (2,i), color))
    score_table.setStyle(TableStyle(table_style))
    story.append(score_table)
    story.append(Spacer(1, 6*mm))

    # Per framework
    for fw, result in scored_results.items():
        fw_name = result.get('framework_name', fw)
        score = result.get('score', 0)
        label = result.get('label', '')

        fw_header = Table([[
            Paragraph(f'<b>{fw_name}</b>',
                ParagraphStyle('fw', fontSize=10, fontName='Helvetica-Bold', textColor=white)),
            Paragraph(f'<b>{score}/100 — {label}</b>',
                ParagraphStyle('sc', fontSize=10, fontName='Helvetica-Bold',
                              textColor=TEAL, alignment=TA_RIGHT))
        ]], colWidths=[110*mm, 60*mm])
        fw_header.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), DARK),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(fw_header)

        if 'error' in result:
            story.append(Paragraph(f"Error: {result['error']}",
                ParagraphStyle('err', fontSize=9, textColor=RED)))
            story.append(Spacer(1, 4*mm))
            continue

        analysis = result.get('analysis', '')
        passed = extract_section(analysis, "PASSED CHECKS")
        failed = extract_section(analysis, "FAILED CHECKS")
        gaps = extract_section(analysis, "GAP ANALYSIS")
        fixes = extract_section(analysis, "RECOMMENDED FIXES")

        cell = ParagraphStyle('cell', fontSize=8, leading=12)
        green = ParagraphStyle('g', fontSize=8, leading=12, textColor=GREEN)
        red = ParagraphStyle('r', fontSize=8, leading=12, textColor=RED)
        orange = ParagraphStyle('o', fontSize=8, leading=12, textColor=ORANGE)

        if passed:
            story.append(Spacer(1, 2*mm))
            story.append(Paragraph('PASSED CHECKS',
                ParagraphStyle('sh', fontSize=9, fontName='Helvetica-Bold', textColor=GREEN)))
            for item in passed:
                story.append(Paragraph(f'  [PASS]  {item}', green))

        if failed:
            story.append(Spacer(1, 2*mm))
            story.append(Paragraph('FAILED CHECKS',
                ParagraphStyle('sh', fontSize=9, fontName='Helvetica-Bold', textColor=RED)))
            for item in failed:
                story.append(Paragraph(f'  [FAIL]  {item}', red))

        if gaps:
            story.append(Spacer(1, 2*mm))
            story.append(Paragraph('GAP ANALYSIS',
                ParagraphStyle('sh', fontSize=9, fontName='Helvetica-Bold', textColor=ORANGE)))
            for item in gaps:
                story.append(Paragraph(f'  >  {item}', orange))

        if fixes:
            story.append(Spacer(1, 2*mm))
            story.append(Paragraph('RECOMMENDED FIXES',
                ParagraphStyle('sh', fontSize=9, fontName='Helvetica-Bold', textColor=DARK)))
            for i, item in enumerate(fixes, 1):
                story.append(Paragraph(f'  {i}.  {item}', cell))

        story.append(Spacer(1, 6*mm))

    # Disclaimer
    story.append(HRFlowable(width="100%", thickness=1, color=MEDIUM_GRAY))
    story.append(Spacer(1, 3*mm))
    disclaimer = Table([[
        Paragraph(
            'DISCLAIMER: This report is DRAFT — Awaiting Auditor Review. '
            'AuditX outputs are AI-assisted analysis only. They are not legal opinions, '
            'compliance certificates, or legal advice. Always verify with a qualified '
            'compliance professional. ByteFortix Security accepts no liability for '
            'decisions made based on this report.',
            ParagraphStyle('disc', fontSize=7.5, textColor=HexColor('#78350f'), leading=11)
        )
    ]], colWidths=[170*mm])
    disclaimer.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#fffbeb')),
        ('BOX', (0,0), (-1,-1), 1, HexColor('#fbbf24')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(disclaimer)
    doc.build(story)
    return filename

if __name__ == "__main__":
    dummy = {
        "dpdp": {
            "framework_name": "DPDP Act 2023",
            "score": 70, "label": "MEDIUM RISK",
            "analysis": """COMPLIANCE SCORE: 70

PASSED CHECKS:
- Company collects data with stated purpose
- Users can request deletion

FAILED CHECKS:
- No consent mechanism mentioned
- No Data Protection Officer named

GAP ANALYSIS:
- Missing explicit consent collection at signup
- No DPO contact information provided

RECOMMENDED FIXES:
- Add consent checkbox at registration
- Appoint a Data Protection Officer"""
        }
    }
    overall = {"score": 70, "label": "MEDIUM RISK"}
    path = generate_pdf_report(dummy, overall, "Test Hospital Pvt Ltd")
    print(f"PDF saved to: {path}")
