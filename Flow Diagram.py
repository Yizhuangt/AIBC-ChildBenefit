import streamlit as st

st.set_page_config(page_title="Application Flow Diagram", page_icon="🔀", layout="wide")

if not st.session_state.get("password_correct", False):
    st.warning("Please log in from the main page.")
    st.stop()

st.title("Application Flow Diagram")
st.caption("This page shows how the different components of the application work together.")

st.subheader("Overall Application Flow")
st.code("""
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
""", language=None)

st.divider()

st.subheader("Page-by-Page Flow")

tab1, tab2, tab3 = st.tabs(["Cash Gifts & Grants RAG", "Ask Me Anything", "Benefit Advisory"])

with tab1:
    st.markdown("#### Cash Gifts & Grants RAG")
    st.code("""
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
    """, language=None)
    st.markdown("""
    **Data Sources:** 3 locally stored `.mhtml` files in `RAG/` folder
    - Baby Bonus Scheme (LifeSG)
    - Large Families Scheme (LifeSG)
    - SG Child Support Package (LifeSG)
    """)

with tab2:
    st.markdown("#### Ask Me Anything")
    st.code("""
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
    """, language=None)
    st.markdown("""
    **Data Sources:** All 15 URLs from `data/knowledge_base.json`, scraped live
    - LifeSG, IRAS, MSF, ECDA, MOE, CPF Board, and more
    """)

with tab3:
    st.markdown("#### Benefit Advisory")
    st.code("""
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
    """, language=None)
    st.markdown("""
    **Data Sources:** Local `data/knowledge_base.json` metadata only (no live scraping)
    - Searches titles, excerpts, tags, and agency fields
    - Falls back to keyword search if no OpenAI API key is set
    """)

st.divider()

st.subheader("Technology Stack")
st.markdown("""
| Component | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | OpenAI GPT-4o-mini |
| Vector Store | Chroma (LangChain) |
| Embeddings | OpenAI text-embedding-3-small |
| Web Scraping | BeautifulSoup + Requests |
| Document Loading | LangChain TextLoader |
| Data Storage | JSON (knowledge_base.json) + MHTML files |
""")
