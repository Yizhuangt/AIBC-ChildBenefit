import streamlit as st
import random
import hmac


def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    if st.session_state.get("password_correct", False):
        return True
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* === Global === */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .main .block-container {
        padding-top: 2rem;
        max-width: 1100px;
    }

    /* === Sidebar === */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #8b7fa0 0%, #a99abb 50%, #bdb0cc 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #faf8fd !important;
    }
    section[data-testid="stSidebar"] .stMarkdown a {
        color: #e8dff5 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown a:hover {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.15);
    }
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        color: #ede8f5 !important;
        border-radius: 8px;
        transition: all 0.2s;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.2);
        border-color: rgba(255,255,255,0.35);
    }

    /* === Headings === */
    h1 {
        color: #5c5070 !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    h2, h3 {
        color: #6b5f80 !important;
        font-weight: 600 !important;
    }

    /* === Primary button === */
    .stButton > button[kind="primary"],
    .stFormSubmitButton > button,
    div[data-testid="stForm"] .stButton > button {
        background: linear-gradient(135deg, #c5ddbf, #b5d1ad) !important;
        color: #3d4f38 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.6rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(181,209,173,0.35) !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button:hover,
    div[data-testid="stForm"] .stButton > button:hover {
        background: linear-gradient(135deg, #b5d1ad, #a5c49c) !important;
        box-shadow: 0 4px 14px rgba(181,209,173,0.45) !important;
        transform: translateY(-1px);
    }

    /* Regular buttons */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        border: 1px solid #d5cde0 !important;
    }
    .stButton > button:hover {
        border-color: #cac0d8 !important;
        color: #7a6e90 !important;
    }

    /* === Tabs === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #cac0d8, #bdb0cc);
        color: white !important;
    }

    /* === DataFrame / Table === */
    .stDataFrame [data-testid="stDataFrameResizable"] {
        border-radius: 10px;
        overflow: hidden;
    }

    /* === Expander === */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #6b5f80;
        border-radius: 10px;
    }

    /* === Metric / number input === */
    .stNumberInput > div > div > input {
        border-radius: 8px !important;
    }
    .stSelectbox > div > div {
        border-radius: 8px !important;
    }
    .stTextInput > div > div > input {
        border-radius: 8px !important;
    }
    .stDateInput > div > div > input {
        border-radius: 8px !important;
    }

    /* === Chat === */
    .stChatMessage {
        border-radius: 12px;
        padding: 1rem 1.2rem;
    }
    .stChatInputContainer {
        border-radius: 12px !important;
    }

    /* === Warning / Info boxes === */
    .stAlert {
        border-radius: 10px;
    }

    /* === Custom HTML components === */
    .hero-banner {
        background: linear-gradient(135deg, #b5a8c8 0%, #c8bdd8 40%, #d8d0e4 100%);
        color: #3d3550;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero-banner h1 {
        color: #4a3f5c !important;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
    }
    .hero-banner p {
        color: #6b5f80;
        font-size: 1.1rem;
        margin: 0;
    }

    .feature-card {
        background: white;
        border: 1px solid #e8e0f0;
        border-radius: 14px;
        padding: 1.8rem 1.5rem;
        height: 100%;
        transition: all 0.25s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-color: #cac0d8;
    }
    .feature-card .icon {
        font-size: 2.2rem;
        margin-bottom: 0.8rem;
    }
    .feature-card h3 {
        color: #5c5070 !important;
        font-size: 1.15rem;
        margin-bottom: 0.5rem;
    }
    .feature-card p {
        color: #8a809a;
        font-size: 0.92rem;
        line-height: 1.55;
    }

    .info-card {
        background: #f9f7fc;
        border: 1px solid #e8e0f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .section-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.3rem;
    }
    .section-header .icon {
        font-size: 1.5rem;
    }
    .section-header h2 {
        margin: 0;
        font-size: 1.4rem;
    }

    .source-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f5f0fa, #ede5f5);
        border: 1px solid #d5cde0;
        border-radius: 8px;
        padding: 0.4rem 0.8rem;
        margin: 0.2rem;
        font-size: 0.82rem;
        color: #7a6e90;
        font-weight: 500;
    }

    .disclaimer-card {
        background: linear-gradient(135deg, #fffbeb, #fef3c7);
        border: 1px solid #fde68a;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-top: 1.5rem;
    }
    .disclaimer-card p {
        color: #92400e;
        font-size: 0.9rem;
        margin: 0;
    }

    .tech-badge {
        display: inline-block;
        background: #f9f7fc;
        border: 1px solid #d5cde0;
        border-radius: 20px;
        padding: 0.3rem 0.8rem;
        font-size: 0.82rem;
        color: #7a6e90;
        font-weight: 500;
        margin: 0.15rem;
    }

    .gradient-divider {
        height: 3px;
        background: linear-gradient(90deg, #cac0d8, #c5ddbf, #cac0d8);
        border: none;
        border-radius: 2px;
        margin: 1.5rem 0;
        opacity: 0.5;
    }

    /* === Login card === */
    .login-card {
        max-width: 420px;
        margin: 3rem auto;
        background: white;
        border: 1px solid #e8e0f0;
        border-radius: 16px;
        padding: 2.5rem 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        text-align: center;
    }
    .login-card h2 {
        color: #5c5070 !important;
        margin-bottom: 0.3rem;
    }
    .login-card p {
        color: #8a809a;
        margin-bottom: 1.5rem;
    }

    /* === Code blocks (for flow diagrams) === */
    .styled-code {
        background: #f3f0f8;
        color: #4a3f5c;
        border-radius: 12px;
        padding: 1.5rem;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 0.82rem;
        line-height: 1.5;
        overflow-x: auto;
        white-space: pre;
        border: 1px solid #ddd5e8;
    }
    </style>
    """, unsafe_allow_html=True)
