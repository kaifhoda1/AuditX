import streamlit as st
import tempfile
import os
from core.extractor import extract_text
from core.analyzer import analyze_policy
from core.scorer import score_all, overall_score
from core.reporter import build_report, save_report
from core.pdf_reporter import generate_pdf_report
from core.word_reporter import generate_word_report
from core.visualizer import create_risk_heatmap

st.set_page_config(
    page_title="AuditX — GRC Compliance",
    page_icon="assets/logo.png" if os.path.exists("assets/logo.png") else None,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

* { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #0a0a0f;
    color: #e2e8f0;
}
.main { background: #0a0a0f; }
.main .block-container { padding: 2rem 2.5rem; max-width: 1300px; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid #1e293b;
}
[data-testid="stSidebar"] * { color: #94a3b8 !important; }
[data-testid="stSidebar"] h3 {
    color: #475569 !important;
    font-size: 0.65rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
[data-testid="stSidebar"] .stTextInput input {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    color: #f1f5f9 !important;
    border-radius: 6px !important;
    font-size: 0.9rem !important;
}
[data-testid="stSidebar"] .stTextInput input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}
[data-testid="stSidebar"] .stCheckbox label {
    font-size: 0.85rem !important;
    color: #94a3b8 !important;
}
[data-testid="stSidebar"] hr { border-color: #1e293b !important; }

/* Top brand bar */
.brand-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem 2rem;
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
    border: 1px solid #1e293b;
    border-radius: 12px;
    margin-bottom: 1.5rem;
}
.brand-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: 6px;
}
.brand-name span { color: #6366f1; }
.brand-sub {
    font-size: 0.72rem;
    color: #475569;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 4px;
}
.brand-badges {
    display: flex;
    gap: 0.5rem;
}
.badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    padding: 0.3rem 0.75rem;
    border-radius: 4px;
    letter-spacing: 1px;
    font-weight: 600;
}
.badge-green { background: #052e16; color: #4ade80; border: 1px solid #166534; }
.badge-blue { background: #0c1a3d; color: #818cf8; border: 1px solid #1e3a8a; }
.badge-gray { background: #1e293b; color: #64748b; border: 1px solid #334155; }

/* Stats */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.stat-box {
    background: #0f0f1a;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.stat-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.stat-box.indigo::before { background: #6366f1; }
.stat-box.green::before { background: #22c55e; }
.stat-box.amber::before { background: #f59e0b; }
.stat-box.slate::before { background: #475569; }
.stat-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1;
}
.stat-label {
    font-size: 0.7rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 0.4rem;
}

/* Upload area */
.upload-card {
    background: #0f0f1a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e293b;
}

/* Score cards */
.scores-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.score-box {
    background: #0f0f1a;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 1.5rem 1rem;
    text-align: center;
}
.score-box.overall { border-color: #6366f1; background: #0c0c1f; }
.score-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.5rem;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1;
}
.score-fw {
    font-size: 0.65rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 0.4rem;
}
.score-risk {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    margin-top: 0.3rem;
}
.risk-low { color: #22c55e; }
.risk-medium { color: #f59e0b; }
.risk-high { color: #ef4444; }
.risk-critical { color: #7f1d1d; }

/* Button */
.stButton > button {
    background: #6366f1 !important;
    color: white !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.65rem 2rem !important;
    letter-spacing: 2px !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #4f46e5 !important;
    transform: translateY(-1px) !important;
}

/* Download buttons */
.stDownloadButton > button {
    background: #0f172a !important;
    color: #94a3b8 !important;
    border: 1px solid #1e293b !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    border-radius: 6px !important;
    width: 100% !important;
    letter-spacing: 1px !important;
}
.stDownloadButton > button:hover {
    border-color: #6366f1 !important;
    color: #818cf8 !important;
}

/* Expander */
details {
    background: #0f0f1a !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    margin-bottom: 0.5rem !important;
}
summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    color: #94a3b8 !important;
    padding: 1rem !important;
}

/* Alerts */
.stSuccess { background: #052e16 !important; border-color: #166534 !important; }
.stWarning { background: #1c1300 !important; border-color: #854d0e !important; }
.stInfo { background: #0c1a3d !important; border-color: #1e3a8a !important; }

/* Disclaimer */
.disclaimer {
    background: #1c1300;
    border: 1px solid #854d0e;
    border-left: 3px solid #f59e0b;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    font-size: 0.78rem;
    color: #92400e;
    margin: 1rem 0;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# Brand bar
st.markdown("""
<div class="brand-bar">
    <div>
        <div class="brand-name">AUDIT<span>X</span></div>
        <div class="brand-sub">ByteFortix Security &nbsp;·&nbsp; Private GRC Intelligence</div>
    </div>
    <div class="brand-badges">
        <span class="badge badge-green">OFFLINE</span>
        <span class="badge badge-blue">MISTRAL 7B</span>
        <span class="badge badge-gray">AIR GAPPED</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### CLIENT")
    company_name = st.text_input("", placeholder="Company name")
    st.markdown("---")
    st.markdown("### FRAMEWORKS")
    use_dpdp = st.checkbox("DPDP Act 2025 (India)", value=True)
    use_gdpr = st.checkbox("GDPR", value=True)
    use_eu_ai = st.checkbox("EU AI Act 2024", value=False)
    use_nist = st.checkbox("NIST 800-53", value=False)
    use_rbi = st.checkbox("RBI Digital Payments", value=False)
    st.markdown("---")
    st.markdown("### SYSTEM")
    st.caption("Model · Mistral 7B")
    st.caption("Vector DB · ChromaDB")
    st.caption("Network · None")
    st.caption("Storage · Local only")
    st.markdown("---")
    st.caption("DRAFT outputs only. Not legal advice.")
    st.caption("ByteFortix Security © 2026")

selected_frameworks = []
if use_dpdp: selected_frameworks.append("dpdp")
if use_gdpr: selected_frameworks.append("gdpr")
if use_eu_ai: selected_frameworks.append("eu_ai_act")
if use_nist: selected_frameworks.append("nist")
if use_rbi: selected_frameworks.append("rbi_digital")

# Stats
st.markdown("""
<div class="stats-grid">
    <div class="stat-box indigo">
        <div class="stat-val">5</div>
        <div class="stat-label">Frameworks</div>
    </div>
    <div class="stat-box green">
        <div class="stat-val">3342</div>
        <div class="stat-label">Knowledge Chunks</div>
    </div>
    <div class="stat-box amber">
        <div class="stat-val">100%</div>
        <div class="stat-label">Local Processing</div>
    </div>
    <div class="stat-box slate">
        <div class="stat-val">0</div>
        <div class="stat-label">Data Exfiltration</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Upload
st.markdown('<div class="section-label">Document Upload</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Upload company policy — PDF or TXT",
    type=["pdf", "txt"],
    label_visibility="collapsed"
)

if uploaded_file and selected_frameworks and company_name:
    if st.button("RUN COMPLIANCE ANALYSIS"):

        with st.spinner("Extracting document..."):
            suffix = ".pdf" if uploaded_file.name.endswith(".pdf") else ".txt"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            try:
                policy_text = extract_text(tmp_path)
                st.success(f"Extracted {len(policy_text):,} characters from {uploaded_file.name}")
            except Exception as e:
                st.error(f"Extraction failed: {e}")
                os.unlink(tmp_path)
                st.stop()
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        with st.spinner(f"Analyzing against {len(selected_frameworks)} framework(s)..."):
            try:
                results = analyze_policy(policy_text, selected_frameworks)
                scored = score_all(results)
                overall = overall_score(scored)
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.stop()

        # Scores
        st.markdown('<div class="section-label">Compliance Scores</div>',
                   unsafe_allow_html=True)

        risk_class = {
            "LOW RISK": "risk-low",
            "MEDIUM RISK": "risk-medium",
            "HIGH RISK": "risk-high",
            "CRITICAL RISK": "risk-critical"
        }

        scores_html = '<div class="scores-grid">'
        oc = risk_class.get(overall['label'], 'risk-medium')
        scores_html += f"""
        <div class="score-box overall">
            <div class="score-num">{overall['score']}</div>
            <div class="score-fw">Overall</div>
            <div class="score-risk {oc}">{overall['label']}</div>
        </div>"""

        for fw, result in scored.items():
            rc = risk_class.get(result.get('label',''), 'risk-medium')
            scores_html += f"""
            <div class="score-box">
                <div class="score-num">{result.get('score',0)}</div>
                <div class="score-fw">{fw.upper()}</div>
                <div class="score-risk {rc}">{result.get('label','')}</div>
            </div>"""
        scores_html += '</div>'
        st.markdown(scores_html, unsafe_allow_html=True)

        # Risk Heatmap
        st.markdown('<div class="section-label">Risk Heatmap</div>', unsafe_allow_html=True)
        fig = create_risk_heatmap(scored)
        st.plotly_chart(fig, use_container_width=True)

        # Analysis
        st.markdown('<div class="section-label">Detailed Analysis</div>',
                   unsafe_allow_html=True)
        for framework, result in scored.items():
            fw_name = result.get("framework_name", framework)
            score = result.get("score", 0)
            label = result.get("label", "")
            with st.expander(f"{fw_name}  |  {score}/100  |  {label}"):
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.markdown(result["analysis"])

        # Disclaimer
        st.markdown("""
        <div class="disclaimer">
        DRAFT — Awaiting Auditor Review. This is AI-assisted analysis only.
        Not a legal opinion or compliance certificate.
        Always verify with a qualified compliance professional.
        </div>""", unsafe_allow_html=True)

        # Export
        st.markdown('<div class="section-label">Export Report</div>',
                   unsafe_allow_html=True)
        report_text = build_report(scored, overall, company_name)
        report_path = save_report(report_text, company_name)
        pdf_path = generate_pdf_report(scored, overall, company_name)

        col1, col2 = st.columns(2)
        with col1:
            with open(report_path, "r") as f:
                st.download_button(
                    label="DOWNLOAD TXT REPORT",
                    data=f.read(),
                    file_name=os.path.basename(report_path),
                    mime="text/plain"
                )
        with col2:
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="DOWNLOAD PDF REPORT",
                    data=f.read(),
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf"
                )
        col3, col4 = st.columns(2)
        with col3:
            word_path = generate_word_report(scored, overall, company_name)
            with open(word_path, "rb") as f:
                st.download_button(
                    label="DOWNLOAD WORD REPORT",
                    data=f.read(),
                    file_name=os.path.basename(word_path),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

elif uploaded_file and not company_name:
    st.warning("Enter company name in the sidebar.")
elif uploaded_file and not selected_frameworks:
    st.warning("Select at least one framework.")
else:
    st.markdown("""
    <div style="background:#0f0f1a;border:1px solid #1e293b;border-radius:12px;
    padding:4rem 2rem;text-align:center;margin-top:1rem;">
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.9rem;
        color:#334155;letter-spacing:4px;">READY FOR ANALYSIS</div>
        <div style="color:#1e293b;font-size:0.8rem;margin-top:0.75rem;letter-spacing:1px;">
            Enter company name &nbsp;→&nbsp; Select frameworks &nbsp;→&nbsp;
            Upload policy &nbsp;→&nbsp; Run analysis
        </div>
    </div>
    """, unsafe_allow_html=True)
