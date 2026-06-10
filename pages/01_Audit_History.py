import streamlit as st
from auth import check_auth
from database import get_all_audits, get_audit_stats, get_client_audits
import json

check_auth()

st.set_page_config(page_title="Audit History — AuditX", layout="wide")

st.markdown("""
<style>
html, body, [class*="css"] { background: #0a0a0f; font-family: 'Inter', sans-serif; color: #e2e8f0; }
.main { background: #0a0a0f; }
.main .block-container { padding: 2rem 2.5rem; max-width: 1300px; }
[data-testid="stSidebar"] { background: #0f0f1a !important; }
[data-testid="stSidebar"] * { color: #94a3b8 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("## Audit History")

stats = get_audit_stats()
col1, col2, col3 = st.columns(3)
col1.metric("Total Audits", stats['total_audits'])
col2.metric("Clients Audited", stats['total_clients'])
col3.metric("Average Score", f"{stats['avg_score']}/100")

st.markdown("---")

audits = get_all_audits()
if not audits:
    st.info("No audits yet. Run your first analysis from the main page.")
else:
    import pandas as pd
    rows = []
    for a in audits:
        frameworks = json.loads(a[5]) if a[5] else []
        rows.append({
            "Client": a[2],
            "Score": f"{a[3]}/100",
            "Risk Level": a[4],
            "Frameworks": ", ".join(frameworks).upper(),
            "Date": a[9]
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

st.sidebar.markdown("---")
if st.sidebar.button("LOGOUT"):
    st.session_state["authenticated"] = False
    st.rerun()
st.sidebar.caption(f"Logged in as: {st.session_state.get('username', 'unknown')}")
