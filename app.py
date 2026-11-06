import streamlit as st
from utility import check_password

st.set_page_config(page_title="About Us", page_icon="ℹ️", layout="wide")

if not check_password():
    st.stop()

st.title("About Us")

st.markdown("""
### Singapore Family Benefits Advisor

This application helps Singapore families understand and explore the government benefits
they may be eligible for. It uses a RAG (Retrieval-Augmented Generation) approach —
fetching live data from official government websites and using AI to summarise and
answer your questions.

---

### What This App Does

- **Cash Gifts & Grants** — Enter your children's details to see a breakdown of Baby Bonus
  cash gifts, CDA First Step Grant, CDA matching, MediSave grants, and a year-by-year timeline.
- **Benefits Explorer** — Ask any question about Singapore family benefits and get answers
  based on official government sources, with follow-up conversation support.

---

### How to Use This App

Use the **sidebar** on the left to navigate between pages:

1. **Cash Gifts and Grants RAG**
   - Enter the number of children you have
   - Fill in each child's date of birth and citizenship
   - Click **"Show my Cash Gifts & Grants"**
   - View the summary table, year-by-year timeline, and charts showing your family's benefits from birth to age 12

2. **Ask Me Anything**
   - Type any question about Singapore family benefits in the chat box
   - The app scrapes the latest information from official government websites and uses AI to answer
   - Ask follow-up questions — the conversation remembers your previous questions

3. **Benefit Advisory**
   - Type a question about a specific scheme, eligibility, or historical rules
   - The app searches the local knowledge base and retrieves relevant entries to answer your question

**Tips:**
- For best results, be specific in your questions (e.g. "I have 2 children born in 2020 and 2023, what cash gifts am I eligible for?")
- All pages require login — enter your password on this page first
- Information is AI-generated — always verify with official sources before making decisions

---

### Data Sources

All information is retrieved from official Singapore government websites including:

- [CPF Board](https://www.cpf.gov.sg/) — MediSave Grant for Newborns
- [ECDA](https://www.ecda.gov.sg/) — Preschool Subsidies
- [IRAS](https://www.iras.gov.sg/) — Parenthood Tax Rebate, Qualifying Child Relief, Working Mother's Child Relief
- [LifeSG](https://www.life.gov.sg/) — Baby Bonus, Child Support Package, Large Families Scheme
- [MOE](https://www.moe.gov.sg/) — Edusave and Financial Assistance
- [MSF Pro-Family Leave](https://www.profamilyleave.msf.gov.sg/) — Maternity, Paternity, Shared Parental Leave
- [National Archives of Singapore](https://www.nas.gov.sg/archivesonline/) — Historical government announcements and policy documents

---

### Disclaimer

This is a research aid and planning tool, **not an official government service**.
Information is summarised by AI and may not always be accurate or up to date.
Always verify with the official government sources before making financial decisions.

---
""")
