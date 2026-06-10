import streamlit as st
import hashlib
import os

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Default credentials — change these
USERS = {
    "admin": hash_password("bytefortix2026"),
    "kaif": hash_password("auditx2026"),
}

def login_page():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] {
        background: #0a0a0f;
        font-family: 'Inter', sans-serif;
    }
    .main { background: #0a0a0f; }
    .main .block-container {
        max-width: 420px;
        margin: auto;
        padding-top: 8rem;
    }
    .login-box {
        background: #0f0f1a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 2.5rem;
        text-align: center;
    }
    .login-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #f1f5f9;
        letter-spacing: 6px;
    }
    .login-title span { color: #6366f1; }
    .login-sub {
        font-size: 0.72rem;
        color: #475569;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 4px;
        margin-bottom: 2rem;
    }
    [data-testid="stTextInput"] input {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        color: #f1f5f9 !important;
        border-radius: 6px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    .stButton > button {
        background: #6366f1 !important;
        color: white !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 6px !important;
        width: 100% !important;
        padding: 0.65rem !important;
        letter-spacing: 2px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-box">
        <div class="login-title">AUDIT<span>X</span></div>
        <div class="login-sub">ByteFortix Security · Private GRC Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter username")
    password = st.text_input("Password", type="password", placeholder="Enter password")

    if st.button("LOGIN"):
        if username in USERS and USERS[username] == hash_password(password):
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
