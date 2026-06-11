# Accurate DPDP Act 2023 Section Reference Map
# Source: Digital Personal Data Protection Act 2023 (No. 22 of 2023)

DPDP_SECTIONS = {
    "1": "Short title and commencement",
    "2": "Definitions",
    "3": "Application of Act",
    "4": "Grounds for processing personal data — lawful purpose with consent or legitimate use",
    "5": "Notice — Data Fiduciary must give clear notice before collecting data",
    "6": "Consent — must be free, specific, informed, unconditional and unambiguous",
    "7": "Certain legitimate uses without consent — medical emergency, state functions, employment",
    "8": "General obligations of Data Fiduciary — accuracy, security, grievance redressal",
    "9": "Processing of personal data of children — verifiable parental consent required",
    "10": "Additional obligations of Significant Data Fiduciary — DPO, DPIA, audits",
    "11": "Right of Data Principal to access information about personal data",
    "12": "Right of Data Principal to correction and erasure of personal data",
    "13": "Right of Data Principal to grievance redressal",
    "14": "Right of Data Principal to nominate another person",
    "15": "Duties of Data Principal",
    "16": "Exemptions — certain processing exempt from Act provisions",
    "17": "Exemptions for research, archiving, statistical purposes",
    "18": "Establishment of Data Protection Board of India",
    "19": "Appointment of Chairperson and Members of Board",
    "20": "Functions of Board — inquiries, directions, penalties",
    "21": "Powers of Board",
    "22": "Appeals to Appellate Tribunal",
    "23": "Civil court jurisdiction barred",
    "24": "Penalty for breach of obligations — up to INR 250 crore",
    "25": "Penalty for failure to notify breach — up to INR 200 crore",
    "26": "Penalty for non-compliance with Board directions",
    "27": "General penalties",
    "28": "Factors considered for penalty determination",
    "29": "No penalty without opportunity of being heard",
    "30": "Recovery of penalty",
    "31": "Offences — false information, impersonation",
    "32": "Offences by companies",
    "33": "Compounding of offences",
    "34": "Protection of action in good faith",
    "35": "Power of Central Government to issue directions",
    "36": "Power of Central Government to exempt certain processing",
    "37": "Power to make rules",
    "38": "Rules to be laid before Parliament",
    "39": "Directions by Central Government",
    "40": "Power of Board to issue directions",
    "41": "Amendments to other Acts",
    "42": "Repeal and savings",
}

DPDP_PENALTIES = {
    "4": "Penalty up to INR 50 crore for processing without lawful basis",
    "5": "Penalty up to INR 50 crore for failure to provide notice",
    "6": "Penalty up to INR 250 crore for consent violations",
    "8": "Penalty up to INR 250 crore for breach of Data Fiduciary obligations",
    "9": "Penalty up to INR 200 crore for violations related to children data",
    "10": "Penalty up to INR 150 crore for Significant Data Fiduciary violations",
    "25": "Penalty up to INR 200 crore for failure to notify data breach",
}

def get_section_reference(section_num):
    section_num = str(section_num)
    title = DPDP_SECTIONS.get(section_num, "Unknown section")
    penalty = DPDP_PENALTIES.get(section_num, "")
    ref = f"DPDP Act 2023, Section {section_num} — {title}"
    if penalty:
        ref += f" | {penalty}"
    return ref

def get_reference_context():
    """Returns a formatted reference guide for the LLM prompt."""
    # Only include sections relevant to Data Fiduciary obligations
    relevant_sections = ["2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","24","25"]
    lines = ["DPDP ACT 2023 — DATA FIDUCIARY OBLIGATIONS (cite ONLY these sections for company/clinic audits):"]
    for num, title in DPDP_SECTIONS.items():
        if num not in relevant_sections: continue
        penalty = DPDP_PENALTIES.get(num, "")
        line = f"Section {num}: {title}"
        if penalty:
            line += f" [{penalty}]"
        lines.append(line)
    return "\n".join(lines)

if __name__ == "__main__":
    print(get_reference_context())
