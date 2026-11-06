import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from utility import inject_custom_css

st.set_page_config(page_title="Application Flow Diagram", page_icon="🔀", layout="wide")
inject_custom_css()

if not st.session_state.get("password_correct", False):
    st.warning("Please log in from the main page.")
    st.stop()

st.markdown("""
<div class="section-header">
    <span class="icon">🔀</span>
    <h2>Application Flow Diagram</h2>
</div>
""", unsafe_allow_html=True)
st.caption("This page shows how the different components of the application work together.")

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="section-header">
    <span class="icon">🏗️</span>
    <h2>Overall Application Flow</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="styled-code">
┌─────────────────────────────────────────────────────┐
│                    User visits app                    │
│                    (app.py)                           │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │  Password Check │
              │  (utility.py)   │
              └───────┬────────┘
                      │
            ┌─────────┴─────────┐
            │                   │
          ✗ Denied           ✓ Authenticated
            │                   │
         st.stop()              ▼
                    ┌───────────────────────┐
                    │   About Us / Home      │
                    │   (app.py)             │
                    └───────────┬───────────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
        ┌───────────────┐ ┌─────────┐ ┌──────────────┐
        │ Cash Gifts &  │ │ Ask Me  │ │   Benefit    │
        │ Grants RAG    │ │Anything │ │  Advisory    │
        └───────┬───────┘ └────┬────┘ └──────┬───────┘
                │              │              │
                ▼              ▼              ▼
        ┌──────────────┐ ┌──────────┐ ┌─────────────┐
        │ RAG Pipeline │ │ Web      │ │ Knowledge   │
        │ (MHTML docs) │ │ Scraping │ │ Base JSON   │
        └──────┬───────┘ └────┬─────┘ └──────┬──────┘
               │              │              │
               ▼              ▼              ▼
        ┌─────────────────────────────────────────┐
        │            OpenAI GPT-4o-mini            │
        └─────────────────────────────────────────┘
               │              │              │
               ▼              ▼              ▼
        ┌─────────────────────────────────────────┐
        │          Response displayed to user       │
        └─────────────────────────────────────────┘
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="section-header">
    <span class="icon">📄</span>
    <h2>Page-by-Page Flow</h2>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💰 Cash Gifts & Grants RAG", "💬 Ask Me Anything", "📋 Benefit Advisory"])

with tab1:
    st.markdown("""
    <div class="section-header">
        <span class="icon">💰</span>
        <h2>Cash Gifts & Grants RAG</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
<div class="styled-code">
    User Input                    RAG Pipeline                    Output
    ──────────                    ────────────                    ──────

    ┌──────────────┐
    │ Enter number │
    │ of children  │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Enter DOB &  │
    │ citizenship  │
    │ per child    │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐      ┌────────────────────┐
    │ Click "Show  │─────▶│ Load .mhtml files   │
    │ my benefits" │      │ from RAG/ folder    │
    └──────────────┘      └─────────┬──────────┘
                                    │
                                    ▼
                          ┌────────────────────┐
                          │ Split into chunks   │
                          │ (1000 chars each)   │
                          └─────────┬──────────┘
                                    │
                                    ▼
                          ┌────────────────────┐
                          │ Embed into Chroma   │
                          │ vector store        │
                          └─────────┬──────────┘
                                    │
                                    ▼
                          ┌────────────────────┐
                          │ Retrieve top 10     │
                          │ relevant chunks     │
                          └─────────┬──────────┘
                                    │
                                    ▼
                          ┌────────────────────┐      ┌──────────────────┐
                          │ Send chunks +       │─────▶│ Grants summary   │
                          │ family details      │      │ table             │
                          │ to OpenAI           │      ├──────────────────┤
                          └────────────────────┘      │ Year-by-year     │
                                                      │ timeline table   │
                                                      ├──────────────────┤
                                                      │ Bar chart        │
                                                      ├──────────────────┤
                                                      │ Cumulative line  │
                                                      │ chart            │
                                                      └──────────────────┘
</div>
    """, unsafe_allow_html=True)
    st.markdown("")
    st.markdown("""
    <div class="info-card">
        <strong>📁 Data Sources:</strong> 3 locally stored <code>.mhtml</code> files in <code>RAG/</code> folder
        <ul style="color: #475569; font-size: 0.9rem; margin-top: 0.5rem;">
            <li>Baby Bonus Scheme (LifeSG)</li>
            <li>Large Families Scheme (LifeSG)</li>
            <li>SG Child Support Package (LifeSG)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="section-header">
        <span class="icon">💬</span>
        <h2>Ask Me Anything</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
<div class="styled-code">
    User Input                    Processing                      Output
    ──────────                    ──────────                      ──────

    ┌──────────────┐
    │ Type question │
    │ in chat box   │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐      ┌────────────────────┐
    │ First message │─────▶│ Fetch all URLs from │
    │ triggers      │      │ knowledge_base.json │
    │ source load   │      └─────────┬──────────┘
    └──────────────┘                │
                                    ▼
                          ┌────────────────────┐
                          │ Scrape each URL     │
                          │ with BeautifulSoup  │
                          │ (cached 1 hour)     │
                          └─────────┬──────────┘
                                    │
                                    ▼
                          ┌────────────────────┐
                          │ Build system prompt │
                          │ + scraped context   │
                          │ + chat history      │
                          └─────────┬──────────┘
                                    │
                                    ▼
                          ┌────────────────────┐      ┌──────────────────┐
                          │ Send to OpenAI      │─────▶│ AI response in   │
                          │ (full conversation) │      │ chat interface   │
                          └────────────────────┘      └──────────────────┘
                                                              │
                                                              ▼
                                                      ┌──────────────────┐
                                                      │ User can ask     │
                                                      │ follow-up        │
                                                      │ questions        │
                                                      └──────────────────┘
</div>
    """, unsafe_allow_html=True)
    st.markdown("")
    st.markdown("""
    <div class="info-card">
        <strong>🌐 Data Sources:</strong> All 15 URLs from <code>data/knowledge_base.json</code>, scraped live
        <ul style="color: #475569; font-size: 0.9rem; margin-top: 0.5rem;">
            <li>LifeSG, IRAS, MSF, ECDA, MOE, CPF Board, and more</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div class="section-header">
        <span class="icon">📋</span>
        <h2>Benefit Advisory</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
<div class="styled-code">
    User Input                    Processing                      Output
    ──────────                    ──────────                      ──────

    ┌──────────────┐
    │ Type question │
    │ in text area  │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐      ┌────────────────────┐
    │ Click "Ask   │─────▶│ Load entries from   │
    │ advisor"     │      │ knowledge_base.json │
    └──────────────┘      └─────────┬──────────┘
                                    │
                                    ▼
                          ┌────────────────────┐
                          │ Keyword / embedding │
                          │ search on metadata  │
                          │ (title, excerpt,    │
                          │  tags, agency)      │
                          └─────────┬──────────┘
                                    │
                                    ▼
                          ┌────────────────────┐
                          │ Retrieve top 4      │
                          │ matching entries    │
                          └─────────┬──────────┘
                                    │
                                    ▼
                          ┌────────────────────┐      ┌──────────────────┐
                          │ Send entries to     │─────▶│ AI-generated     │
                          │ OpenAI as context   │      │ answer with      │
                          └────────────────────┘      │ citations [1][2] │
                                                      ├──────────────────┤
                                                      │ Source cards     │
                                                      │ with links       │
                                                      └──────────────────┘
</div>
    """, unsafe_allow_html=True)
    st.markdown("")
    st.markdown("""
    <div class="info-card">
        <strong>📦 Data Sources:</strong> Local <code>data/knowledge_base.json</code> metadata only (no live scraping)
        <ul style="color: #475569; font-size: 0.9rem; margin-top: 0.5rem;">
            <li>Searches titles, excerpts, tags, and agency fields</li>
            <li>Falls back to keyword search if no OpenAI API key is set</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="section-header">
    <span class="icon">⚙️</span>
    <h2>Technology Stack</h2>
</div>
""", unsafe_allow_html=True)

tech = [
    ("Frontend", "Streamlit"),
    ("LLM", "OpenAI GPT-4o-mini"),
    ("Vector Store", "Chroma (LangChain)"),
    ("Embeddings", "OpenAI text-embedding-3-small"),
    ("Web Scraping", "BeautifulSoup + Requests"),
    ("Document Loading", "LangChain TextLoader"),
    ("Data Storage", "JSON + MHTML files"),
]

cols = st.columns(len(tech))
for col, (label, value) in zip(cols, tech):
    with col:
        st.markdown(f"""
        <div class="info-card" style="text-align: center; padding: 1rem 0.5rem;">
            <p style="color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.3rem;">{label}</p>
            <p style="color: #1a3a4a; font-weight: 600; font-size: 0.85rem; margin: 0;">{value}</p>
        </div>
        """, unsafe_allow_html=True)
