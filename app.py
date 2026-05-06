import streamlit as st
import tempfile
import os
from core.extractor import extract_text
from core.analyzer import analyze_policy
from core.scorer import score_all, overall_score
from core.reporter import build_report, save_report

st.set_page_config(
    page_title="AuditX — GRC Compliance",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #f4f5f7;
    color: #1a1a2e;
}

.main { background-color: #f4f5f7; }

.header-box {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    padding: 2rem 2.5rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
}

.header-box h1 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.4rem;
    font-weight: 600;
    margin: 0;
    letter-spacing: 2px;
    color: #00d4aa;
}

.header-box p {
    margin: 0.3rem 0 0 0;
    font-size: 0.9rem;
    color: #a0b4c0;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.status-bar {
    background: #1a1a2e;
    color: #00d4aa;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    margin-bottom: 1.5rem;
    letter-spacing: 1px;
}

.metric-card {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    border-left: 5px solid #00d4aa;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    text-align: center;
}

.metric-card .score {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.5rem;
    font-weight: 700;
    color: #1a1a2e;
}

.metric-card .label {
    font-size: 0.8rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.risk-low { border-left-color: #00c853 !important; }
.risk-medium { border-left-color: #ff9800 !important; }
.risk-high { border-left-color: #f44336 !important; }
.risk-critical { border-left-color: #7b0000 !important; }

.section-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    color: #203a43;
    text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 2px solid #00d4aa;
    padding-bottom: 0.4rem;
    margin-bottom: 1rem;
}

.disclaimer {
    background: #fff8e1;
    border-left: 4px solid #ffc107;
    padding: 0.75rem 1rem;
    border-radius: 4px;
    font-size: 0.8rem;
    color: #5d4037;
    margin-top: 1rem;
}

[data-testid="stSidebar"] {
    background: #1a1a2e !important;
}

[data-testid="stSidebar"] * {
    color: #e0e0e0 !important;
}

[data-testid="stSidebar"] .stCheckbox label {
    color: #a0b4c0 !important;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
}

.stButton > button {
    background: linear-gradient(135deg, #0f2027, #2c5364);
    color: #00d4aa;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    border: 1px solid #00d4aa;
    border-radius: 6px;
    padding: 0.6rem 2rem;
    letter-spacing: 1px;
    width: 100%;
}

.stButton > button:hover {
    background: #00d4aa;
    color: #1a1a2e;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-box">
    <h1>🔐 AUDITX</h1>
    <p>ByteFortix Security — AI-Powered GRC Compliance Analysis</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="status-bar">
▶ MODEL: MISTRAL 7B &nbsp;|&nbsp; RUNTIME: OLLAMA LOCAL &nbsp;|&nbsp; MODE: OFFLINE — AIR GAPPED &nbsp;|&nbsp; DATA EXFILTRATION: DISABLED
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🏢 CLIENT DETAILS")
    company_name = st.text_input("Company Name", placeholder="e.g. City Care Hospital")

    st.markdown("---")
    st.markdown("### 📋 FRAMEWORKS")
    use_dpdp = st.checkbox("DPDP Act 2025 (India)", value=True)
    use_gdpr = st.checkbox("GDPR", value=True)
    use_eu_ai = st.checkbox("EU AI Act 2024", value=False)
    use_nist = st.checkbox("NIST 800-53", value=False)
    use_rbi = st.checkbox("RBI Digital Payments", value=False)

    st.markdown("---")
    st.markdown("### ⚙️ SYSTEM")
    st.markdown("**Model:** Mistral 7B")
    st.markdown("**Storage:** Local ChromaDB")
    st.markdown("**Network:** None")
    st.markdown("---")
    st.caption("⚠️ DRAFT outputs only. Not legal advice.")

# Build frameworks list
selected_frameworks = []
if use_dpdp: selected_frameworks.append("dpdp")
if use_gdpr: selected_frameworks.append("gdpr")
if use_eu_ai: selected_frameworks.append("eu_ai_act")
if use_nist: selected_frameworks.append("nist")
if use_rbi: selected_frameworks.append("rbi_digital")

# Main content
st.markdown('<p class="section-title">Upload Policy Document</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload company policy — PDF or TXT",
    type=["pdf", "txt"]
)

if uploaded_file and selected_frameworks and company_name:
    if st.button("▶ RUN COMPLIANCE ANALYSIS"):
        with st.spinner("Extracting document text..."):
            suffix = ".pdf" if uploaded_file.name.endswith(".pdf") else ".txt"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            try:
                policy_text = extract_text(tmp_path)
                st.success(f"✓ Extracted {len(policy_text):,} characters")
            except Exception as e:
                st.error(f"Extraction failed: {e}")
                os.unlink(tmp_path)
                st.stop()
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        with st.spinner(f"Analyzing against {len(selected_frameworks)} framework(s)... Please wait."):
            try:
                results = analyze_policy(policy_text, selected_frameworks)
                scored = score_all(results)
                overall = overall_score(scored)
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.stop()

        # Results header
        st.markdown("---")
        st.markdown('<p class="section-title">Compliance Results</p>', unsafe_allow_html=True)

        # Score cards
        cols = st.columns(len(scored) + 1)

        risk_class = {
            "LOW RISK": "risk-low",
            "MEDIUM RISK": "risk-medium",
            "HIGH RISK": "risk-high",
            "CRITICAL RISK": "risk-critical"
        }

        with cols[0]:
            rc = risk_class.get(overall['label'], '')
            st.markdown(f"""
            <div class="metric-card {rc}">
                <div class="score">{overall['score']}</div>
                <div class="label">Overall Score</div>
                <div style="font-size:0.75rem;color:#333;margin-top:0.3rem">{overall['label']}</div>
            </div>""", unsafe_allow_html=True)

        for i, (fw, result) in enumerate(scored.items()):
            with cols[i+1]:
                rc = risk_class.get(result.get('label',''), '')
                st.markdown(f"""
                <div class="metric-card {rc}">
                    <div class="score">{result.get('score',0)}</div>
                    <div class="label">{fw.upper()}</div>
                    <div style="font-size:0.75rem;color:#333;margin-top:0.3rem">{result.get('label','')}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Framework details
        st.markdown('<p class="section-title">Detailed Analysis</p>', unsafe_allow_html=True)
        for framework, result in scored.items():
            fw_name = result.get("framework_name", framework)
            score = result.get("score", 0)
            label = result.get("label", "")
            with st.expander(f"📋 {fw_name} — {score}/100 | {label}"):
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.markdown(result["analysis"])

        # Disclaimer
        st.markdown("""
        <div class="disclaimer">
        ⚠️ <strong>DRAFT — Awaiting Auditor Review.</strong>
        This is AI-assisted analysis based on framework documents.
        It is not a legal opinion, compliance certificate, or substitute for professional legal advice.
        </div>""", unsafe_allow_html=True)

        # Download
        st.markdown("---")
        st.markdown('<p class="section-title">Export Report</p>', unsafe_allow_html=True)
        report_text = build_report(scored, overall, company_name)
        report_path = save_report(report_text, company_name)
        with open(report_path, "r") as f:
            st.download_button(
                label="⬇ DOWNLOAD FULL REPORT (TXT)",
                data=f.read(),
                file_name=os.path.basename(report_path),
                mime="text/plain"
            )

elif uploaded_file and not company_name:
    st.warning("Enter company name in the sidebar.")
elif uploaded_file and not selected_frameworks:
    st.warning("Select at least one framework.")
else:
    st.info("👈 Enter company name → select frameworks → upload policy document → run analysis.")
