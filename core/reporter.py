import re
from datetime import datetime

def extract_section(analysis_text: str, section_name: str) -> list:
    """Extract bullet points from a named section in analysis text."""
    pattern = rf'{section_name}:\s*\n(.*?)(?=\n[A-Z\s]+:|$)'
    match = re.search(pattern, analysis_text, re.DOTALL)
    if not match:
        return []
    block = match.group(1)
    items = re.findall(r'-\s(.+)', block)
    return [item.strip() for item in items if item.strip()]

def build_report(scored_results: dict, overall: dict, company_name: str = "Unknown Company") -> str:
    """Build a full text gap report from scored results."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = []
    lines.append("=" * 60)
    lines.append("AUDITX COMPLIANCE GAP REPORT")
    lines.append("=" * 60)
    lines.append(f"Company      : {company_name}")
    lines.append(f"Generated    : {now}")
    lines.append(f"Overall Score: {overall['score']}/100 — {overall['label']}")
    lines.append("DRAFT - Awaiting Auditor Review")
    lines.append("=" * 60)

    for framework, result in scored_results.items():
        fw_name = result.get("framework_name", framework)
        score = result.get("score", 0)
        label = result.get("label", "UNKNOWN")

        lines.append(f"\n{'─'*60}")
        lines.append(f"FRAMEWORK : {fw_name}")
        lines.append(f"SCORE     : {score}/100 — {label}")
        lines.append(f"{'─'*60}")

        if "error" in result:
            lines.append(f"ERROR: {result['error']}")
            continue

        analysis = result.get("analysis", "")

        passed = extract_section(analysis, "PASSED CHECKS")
        failed = extract_section(analysis, "FAILED CHECKS")
        gaps = extract_section(analysis, "GAP ANALYSIS")
        fixes = extract_section(analysis, "RECOMMENDED FIXES")

        lines.append("\nPASSED CHECKS:")
        if passed:
            for item in passed:
                lines.append(f"  ✓ {item}")
        else:
            lines.append("  None identified")

        lines.append("\nFAILED CHECKS:")
        if failed:
            for item in failed:
                lines.append(f"  ✗ {item}")
        else:
            lines.append("  None identified")

        lines.append("\nGAP ANALYSIS:")
        if gaps:
            for item in gaps:
                lines.append(f"  → {item}")
        else:
            lines.append("  No gaps identified")

        lines.append("\nRECOMMENDED FIXES:")
        if fixes:
            for i, item in enumerate(fixes, 1):
                lines.append(f"  {i}. {item}")
        else:
            lines.append("  No fixes required")

    lines.append(f"\n{'='*60}")
    lines.append("DISCLAIMER: This report is AI-assisted analysis only.")
    lines.append("It is not a legal opinion or compliance certificate.")
    lines.append("Always verify findings with a qualified professional.")
    lines.append("=" * 60)

    return "\n".join(lines)

def save_report(report_text: str, company_name: str = "report") -> str:
    """Save report to outputs/reports/ folder."""
    import os
    os.makedirs("outputs/reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = company_name.replace(" ", "_").lower()
    filename = f"outputs/reports/{safe_name}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text)
    return filename

if __name__ == "__main__":
    # Test reporter
    dummy_scored = {
        "dpdp": {
            "framework_name": "DPDP Act 2023",
            "score": 70,
            "label": "MEDIUM RISK",
            "color": "orange",
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
    overall = {"score": 70, "label": "MEDIUM RISK", "color": "orange"}
    report = build_report(dummy_scored, overall, "Test Hospital Pvt Ltd")
    print(report)
    path = save_report(report, "Test Hospital Pvt Ltd")
    print(f"\nReport saved to: {path}")
