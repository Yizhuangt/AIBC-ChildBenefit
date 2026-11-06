import streamlit as st
from utility import check_password, inject_custom_css

st.set_page_config(page_title="SG Family Benefits Advisor", page_icon="🇸🇬", layout="wide")
inject_custom_css()

if not check_password():
    st.stop()

st.markdown("""
<div class="hero-banner">
    <h1>🇸🇬 Singapore Family Benefits Advisor</h1>
    <p>Explore government benefits for your family — powered by AI and official data sources</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("**💰 Cash Gifts & Grants**")
        st.caption("Enter your children's details to see Baby Bonus cash gifts, CDA grants, MediSave grants, and a year-by-year timeline from birth to age 12.")
        st.page_link("pages/Cash Gifts and Grants RAG.py", label="Open Cash Gifts & Grants →", icon="💰")

with col2:
    with st.container(border=True):
        st.markdown("**💬 Ask Me Anything**")
        st.caption("Ask any question about Singapore family benefits. The app scrapes the latest info from official sources and uses AI to answer — with follow-up support.")
        st.page_link("pages/Ask Me Anything.py", label="Open Ask Me Anything →", icon="💬")

with col3:
    with st.container(border=True):
        st.markdown("**🔀 Application Flow**")
        st.caption("See how the app works under the hood — from data retrieval to AI-powered responses — with interactive architecture diagrams.")
        st.page_link("pages/Flow Diagram.py", label="Open Application Flow →", icon="🔀")

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="section-header">
    <span class="icon">📖</span>
    <h2>How to Use</h2>
</div>
""", unsafe_allow_html=True)

how_col1, how_col2 = st.columns(2)

with how_col1:
    st.markdown("""
    <div class="info-card">
        <strong>💰 Cash Gifts & Grants</strong>
        <ol style="color: #475569; font-size: 0.92rem; padding-left: 1.2rem;">
            <li>Enter the number of children you have</li>
            <li>Fill in each child's date of birth and citizenship</li>
            <li>Click <em>"Show my Cash Gifts & Grants"</em></li>
            <li>View the summary table, timeline, and charts</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

with how_col2:
    st.markdown("""
    <div class="info-card">
        <strong>💬 Ask Me Anything</strong>
        <ol style="color: #475569; font-size: 0.92rem; padding-left: 1.2rem;">
            <li>Type any question about Singapore family benefits</li>
            <li>The app fetches the latest info from official websites</li>
            <li>Get an AI-generated answer with source context</li>
            <li>Ask follow-up questions — conversation history is kept</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.markdown("""
> **Tip:** For best results, be specific — e.g. *"I have 2 children born in 2020 and 2023, what cash gifts am I eligible for?"*
""")

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

with st.expander("📚 Data Sources"):
    st.markdown("""
    All information is retrieved from official Singapore government websites:
    """)
    st.markdown("""
- [CPF Board](https://www.cpf.gov.sg/) — MediSave Grant for Newborns
- [ECDA](https://www.ecda.gov.sg/) — Preschool Subsidies
- [IRAS](https://www.iras.gov.sg/) — Parenthood Tax Rebate, QCR, WMCR
- [LifeSG](https://www.life.gov.sg/) — Baby Bonus, Child Support Package, Large Families Scheme
- [MOE](https://www.moe.gov.sg/) — Edusave & Financial Assistance
- [MSF Pro-Family Leave](https://www.profamilyleave.msf.gov.sg/) — Maternity, Paternity & Shared Parental Leave
- [National Archives](https://www.nas.gov.sg/archivesonline/) — Historical policy documents
    """)

st.markdown("""
<div class="disclaimer-card">
    <p>⚠️ <strong>Disclaimer:</strong> This is a research aid and planning tool, <strong>not an official government service</strong>.
    Information is summarised by AI and may not always be accurate or up to date.
    Always verify with official government sources before making financial decisions.</p>
</div>
""", unsafe_allow_html=True)
