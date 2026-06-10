import streamlit as st
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def get_users():
    return {
        "admin": hash_password(os.getenv("AUDITX_ADMIN_PASS", "")),
        "kaif": hash_password(os.getenv("AUDITX_KAIF_PASS", "")),
    }

def login_page():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@400;600&display=swap');
html, body, [class*="css"] { background: #0a0a0f; font-family: 'Inter', sans-serif; }
.main { background: #0a0a0f; }
.main .block-container { max-width: 420px; margin: auto; padding-top: 8rem; }
[data-testid="stTextInput"] input {
    background: #1e293b !important; border: 1px solid #334155 !important;
    color: #f1f5f9 !important; border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.stButton > button {
    background: #6366f1 !important; color: white !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important; font-weight: 600 !important;
    border: none !important; border-radius: 6px !important;
    width: 100% !important; padding: 0.65rem !important;
    letter-spacing: 2px !important;
}
</style>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="background:#0f0f1a;border:1px solid #1e293b;border-radius:12px;padding:2.5rem;text-align:center;">
    <div style="font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:700;color:#f1f5f9;letter-spacing:6px;">AUDIT<span style="color:#6366f1;">X</span></div>
    <div style="font-size:0.72rem;color:#475569;letter-spacing:2px;text-transform:uppercase;margin-top:4px;margin-bottom:2rem;">ByteFortix Security · Private GRC Intelligence</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    username = st.text_input("Username", placeholder="Enter username")
    password = st.text_input("Password", type="password", placeholder="Enter password")

    if st.button("LOGIN"):
        users = get_users()
        if username in users and users[username] == hash_password(password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("Invalid credentials.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("ByteFortix Security © 2026 — Authorized access only.")

def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if not st.session_state["authenticated"]:
        login_page()
        st.stop()
