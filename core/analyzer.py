import ollama
import chromadb
import os
import sys, os as _os
sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from core.dpdp_reference import get_reference_context

CHROMA_PATH = "chroma_db"
MODEL = "mistral"

FRAMEWORK_NAMES = {
    "dpdp": "Digital Personal Data Protection Act 2023 & Rules 2025 (India)",
    "dpdp_act": "Digital Personal Data Protection Act 2023 (Full Text)",
    "dpdp_rules": "Digital Personal Data Protection Rules 2025 (Full Text)",
    "gdpr": "General Data Protection Regulation (GDPR)",
    "eu_ai_act": "EU Artificial Intelligence Act 2024",
    "nist": "NIST Special Publication 800-53 Rev 5",
    "rbi_digital": "RBI Master Direction on Digital Payment Security Controls",
}

def load_constitution():
    path = "constitution.txt"
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""

def retrieve_context(query, framework, n_results=5):
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        collection = client.get_collection(name=framework)
    except Exception:
        return ""
    results = collection.query(query_texts=[query], n_results=n_results)
    chunks = results["documents"][0] if results["documents"] else []
    return "\n\n---\n\n".join(chunks)

def check_document_quality(policy_text: str) -> dict:
    word_count = len(policy_text.split())
    char_count = len(policy_text)
    if word_count < 50:
        return {"quality": "CRITICAL", "message": f"Document too short ({word_count} words). Minimum 50 words required for meaningful analysis."}
    elif word_count < 200:
        return {"quality": "WARNING", "message": f"Document is very short ({word_count} words). Analysis may be incomplete. A proper policy should be at least 500 words."}
    elif word_count < 500:
        return {"quality": "NOTICE", "message": f"Document is short ({word_count} words). Consider providing a more detailed policy for thorough analysis."}
    else:
        return {"quality": "OK", "message": f"Document length acceptable ({word_count} words)."}

def analyze_policy(policy_text, frameworks):
    constitution = load_constitution()
    results = {}
    for framework in frameworks:
        framework_name = FRAMEWORK_NAMES.get(framework, framework)
        print(f"  Analyzing against {framework_name}...")
        context = retrieve_context(policy_text[:500], framework)
        if not context:
            results[framework] = {"framework_name": framework_name, "error": "No framework data found."}
            continue
        dpdp_ref = get_reference_context() if "dpdp" in framework else ""
        prompt = f"""You are AuditX, a strict professional GRC compliance analysis tool built by ByteFortix Security. Be rigorous and conservative in scoring. A policy missing consent mechanism, DPO, breach notification, retention period, or security measures cannot score above 50. Score based on what is explicitly present in the policy, not what is implied.

SYSTEM RULES:
{constitution}

FRAMEWORK: {framework_name}

RELEVANT FRAMEWORK CLAUSES:
{context}

DPDP EXACT SECTION REFERENCE — ONLY USE THESE SECTION NUMBERS FOR DPDP CITATIONS:
{dpdp_ref}

COMPANY POLICY DOCUMENT:
{policy_text[:3000]}

Analyze the company policy against the framework clauses above.
Be precise. Cite exact article and section numbers for every finding.
Classify every failed check by severity:
- CRITICAL: violation carries penalty above INR 100 crore or exposes sensitive data
- HIGH: violation carries penalty above INR 50 crore or affects data subject rights
- MEDIUM: violation affects compliance posture but lower penalty
- LOW: minor gap, best practice recommendation

Respond in this exact format:

COMPLIANCE SCORE: [0-100]

PASSED CHECKS:
- [Requirement met — cite exact Article/Section e.g. DPDP Section 6(1) or GDPR Article 13(1)]

FAILED CHECKS:
- [CRITICAL/HIGH/MEDIUM/LOW] [Requirement failed — cite exact Article/Section being violated]

GAP ANALYSIS:
- [CRITICAL/HIGH/MEDIUM/LOW] [Specific gap — cite Article/Section and exact penalty amount]

RECOMMENDED FIXES:
- [Priority 1/2/3] [Exact actionable fix — cite Article/Section] [Timeline: immediate/2 weeks/1 month]

DISCLAIMER: DRAFT - Awaiting Auditor Review. This is AI-assisted analysis, not legal advice."""
        try:
            response = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
            results[framework] = {"framework_name": framework_name, "analysis": response["message"]["content"]}
        except Exception as e:
            results[framework] = {"framework_name": framework_name, "error": f"Ollama error: {str(e)}"}
    return results

if __name__ == "__main__":
    sample_policy = """
    Our company collects user email addresses and phone numbers for account registration.
    We store data on our servers. Users can request deletion by emailing support.
    We do not share data with third parties. We use cookies on our website.
    """
    print("=== AuditX Analyzer Test ===\n")
    results = analyze_policy(sample_policy, ["dpdp"])
    for fw, result in results.items():
        print(f"\n{'='*50}")
        print(f"Framework: {result['framework_name']}")
        print('='*50)
        if "error" in result:
            print(f"ERROR: {result['error']}")
        else:
            print(result["analysis"])
