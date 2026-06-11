from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os

DARK = HexColor('#0d1117')
TEAL = HexColor('#00d4aa')
GOLD = HexColor('#f59e0b')
LIGHT = HexColor('#f4f5f7')
GRAY = HexColor('#6b7280')
GREEN = HexColor('#10b981')

def generate_certificate(company_name: str, scored_results: dict, overall: dict) -> str:
    """Generate compliance certificate if overall score >= 80."""

    if overall['score'] < 80:
        return None

    os.makedirs("outputs/certificates", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = company_name.replace(" ", "_").lower()
    cert_id = f"BF-{datetime.now().strftime('%Y%m')}-{abs(hash(company_name)) % 10000:04d}"
    filename = f"outputs/certificates/{safe_name}_certificate_{timestamp}.pdf"

    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        rightMargin=20*mm, leftMargin=20*mm,
        topMargin=15*mm, bottomMargin=15*mm
    )

    story = []

    # Top border
    border = Table([['']], colWidths=[170*mm], rowHeights=[3*mm])
    border.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), TEAL),
    ]))
    story.append(border)
    story.append(Spacer(1, 8*mm))

    # Header
    story.append(Paragraph(
        'BYTEFORTIX SECURITY',
        ParagraphStyle('brand', fontSize=11, fontName='Helvetica-Bold',
                      textColor=GRAY, alignment=TA_CENTER, letterSpacing=4)
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        'CERTIFICATE OF COMPLIANCE GAP ANALYSIS',
        ParagraphStyle('title', fontSize=20, fontName='Helvetica-Bold',
                      textColor=DARK, alignment=TA_CENTER, leading=28)
    ))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        'AI-Powered GRC Compliance Platform',
        ParagraphStyle('sub', fontSize=9, fontName='Helvetica',
                      textColor=GRAY, alignment=TA_CENTER)
    ))
    story.append(Spacer(1, 8*mm))

    # Gold divider
    divider = Table([['']], colWidths=[170*mm], rowHeights=[1*mm])
    divider.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), GOLD)]))
    story.append(divider)
    story.append(Spacer(1, 8*mm))

    # Main body
    story.append(Paragraph(
        'This is to certify that',
        ParagraphStyle('body', fontSize=11, fontName='Helvetica',
                      textColor=GRAY, alignment=TA_CENTER)
    ))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        company_name,
        ParagraphStyle('company', fontSize=26, fontName='Helvetica-Bold',
                      textColor=DARK, alignment=TA_CENTER)
    ))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        'has successfully completed a comprehensive AI-powered compliance gap analysis<br/>'
        'conducted by ByteFortix Security using the AuditX platform.',
        ParagraphStyle('body2', fontSize=10, fontName='Helvetica',
                      textColor=GRAY, alignment=TA_CENTER, leading=16)
    ))
    story.append(Spacer(1, 8*mm))

    # Score box
    score_table = Table([[
        Paragraph(
            f'<b>{overall["score"]}</b><br/><font size="9" color="#6b7280">COMPLIANCE SCORE</font>',
            ParagraphStyle('score', fontSize=36, fontName='Helvetica-Bold',
                          textColor=TEAL, alignment=TA_CENTER, leading=44)
        ),
        Paragraph(
            f'<b>{overall["label"]}</b><br/><font size="9" color="#6b7280">RISK LEVEL</font>',
            ParagraphStyle('risk', fontSize=18, fontName='Helvetica-Bold',
                          textColor=GREEN, alignment=TA_CENTER, leading=28)
        ),
    ]], colWidths=[85*mm, 85*mm])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT),
        ('BOX', (0,0), (-1,-1), 1, HexColor('#e5e7eb')),
        ('PADDING', (0,0), (-1,-1), 12),
        ('LINEAFTER', (0,0), (0,-1), 1, HexColor('#e5e7eb')),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 8*mm))

    # Frameworks
    story.append(Paragraph(
        'FRAMEWORKS AUDITED',
        ParagraphStyle('fwh', fontSize=9, fontName='Helvetica-Bold',
                      textColor=GRAY, alignment=TA_CENTER, letterSpacing=2)
    ))
    story.append(Spacer(1, 3*mm))

    fw_data = []
    for fw, result in scored_results.items():
        fw_data.append([
            result.get('framework_name', fw),
            f"{result.get('score', 0)}/100",
            result.get('label', '')
        ])

    fw_table = Table(fw_data, colWidths=[100*mm, 30*mm, 40*mm])
    fw_table.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('TEXTCOLOR', (0,0), (-1,-1), GRAY),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#e5e7eb')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,-1), LIGHT),
    ]))
    story.append(fw_table)
    story.append(Spacer(1, 8*mm))

    # Gold divider
    story.append(divider)
    story.append(Spacer(1, 6*mm))

    # Certificate details
    now = datetime.now().strftime("%B %d, %Y")
    details = Table([
        ['Certificate ID', cert_id, 'Issue Date', now],
        ['Issued By', 'ByteFortix Security', 'Valid For', '90 days from issue'],
        ['Analysis Method', 'AI-Assisted RAG Pipeline', 'Platform', 'AuditX v1.0'],
    ], colWidths=[35*mm, 55*mm, 35*mm, 45*mm])
    details.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (-1,-1), GRAY),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#e5e7eb')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (0,-1), LIGHT),
        ('BACKGROUND', (2,0), (2,-1), LIGHT),
    ]))
    story.append(details)
    story.append(Spacer(1, 8*mm))

    # Disclaimer
    disclaimer = Table([[
        Paragraph(
            'IMPORTANT DISCLAIMER: This certificate confirms completion of an AI-assisted compliance gap analysis only. '
            'It does not constitute legal advice, a formal compliance certification, or a guarantee of regulatory compliance. '
            'Findings should be reviewed and verified by a qualified legal or compliance professional. '
            'ByteFortix Security accepts no liability for regulatory penalties arising from reliance on this analysis.',
            ParagraphStyle('disc', fontSize=7, textColor=HexColor('#78350f'), leading=10)
        )
    ]], colWidths=[170*mm])
    disclaimer.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#fffbeb')),
        ('BOX', (0,0), (-1,-1), 1, HexColor('#fbbf24')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(disclaimer)
    story.append(Spacer(1, 5*mm))

    # Signature line
    sig = Table([[
        Paragraph('Mohammad Kaif\nFounder, ByteFortix Security\nkaifhoda1@gmail.com',
                 ParagraphStyle('sig', fontSize=8, fontName='Helvetica', textColor=GRAY)),
        Paragraph(f'Certificate ID: {cert_id}\nPowered by AuditX\ngithub.com/kaifhoda1',
                 ParagraphStyle('sig2', fontSize=8, fontName='Helvetica',
                               textColor=GRAY, alignment=TA_CENTER)),
        Paragraph('_____________________\nAuthorized Signatory\nByteFortix Security',
                 ParagraphStyle('sig3', fontSize=8, fontName='Helvetica',
                               textColor=GRAY, alignment=TA_LEFT))
    ]], colWidths=[57*mm, 56*mm, 57*mm])
    sig.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('LINEABOVE', (0,0), (-1,0), 0.5, HexColor('#e5e7eb')),
    ]))
    story.append(sig)

    # Bottom border
    story.append(Spacer(1, 5*mm))
    story.append(border)

    doc.build(story)
    return filename

if __name__ == "__main__":
    dummy = {
        "dpdp": {
            "framework_name": "DPDP Act 2023",
            "score": 85, "label": "LOW RISK",
        }
    }
    overall = {"score": 85, "label": "LOW RISK"}
    path = generate_certificate("City Care Hospital Pvt Ltd", dummy, overall)
    if path:
        print(f"Certificate saved to: {path}")
    else:
        print("Score below 80 — no certificate generated")
