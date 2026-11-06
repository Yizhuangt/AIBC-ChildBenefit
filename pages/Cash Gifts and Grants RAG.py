import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from datetime import date
from utility import inject_custom_css

st.set_page_config(page_title="Baby Cash Gifts & Grants Advisor", page_icon="💰", layout="wide")
inject_custom_css()

if not st.session_state.get("password_correct", False):
    st.warning("Please log in from the main page.")
    st.stop()

from openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAPI_API_KEY"]

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

RAG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "RAG")

filename_list = [
    'Baby Bonus Scheme _ LifeSG – Benefits and support.mhtml',
    'Large Families Scheme _ Family planning – LifeSG.mhtml',
    'SG Child Support Package _ LifeSG.mhtml',
]

@st.cache_resource
def build_retriever():
    docs = []
    for filename in filename_list:
        try:
            loader = TextLoader(os.path.join(RAG_DIR, filename), encoding='utf-8')
            docs.extend(loader.load())
        except Exception:
            continue
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)
    embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')
    vector_store = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings_model,
        collection_name="cash_gifts_grants",
    )
    return vector_store.as_retriever(k=10)

retriever = build_retriever()

st.markdown("""
<div class="section-header">
    <span class="icon">💰</span>
    <h2>Baby Cash Gifts & Grants Advisor</h2>
</div>
""", unsafe_allow_html=True)
st.caption("Enter your children's details below. This page uses RAG — retrieving relevant information from locally stored government documents and using AI to summarise the cash gifts and grants your family is eligible for.")

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="section-header">
    <span class="icon">👶</span>
    <h2>Children's Details</h2>
</div>
""", unsafe_allow_html=True)

count = st.number_input("Number of children", min_value=1, max_value=10, value=1, step=1)

children = []
for i in range(int(count)):
    c1, c2, c3 = st.columns([1, 2, 2])
    with c1:
        st.write(f"**Child {i+1}**")
    with c2:
        dob = st.date_input("Date of birth", value=None, min_value=date(2010, 1, 1), key=f"dob_{i}")
    with c3:
        citizenship = st.selectbox("Citizenship", ["Singapore Citizen", "Not Singapore Citizen"], key=f"cit_{i}")
    children.append({"order": i + 1, "dob": dob, "citizenship": citizenship})

st.markdown("")
if st.button("Show my Cash Gifts & Grants", type="primary"):
    has_valid = any(c["dob"] is not None for c in children)
    if not has_valid:
        st.error("Please enter at least one child's date of birth.")
    else:
        children_desc = []
        for c in children:
            if c["dob"]:
                age_days = (date.today() - c["dob"]).days
                age_str = f"{age_days // 365} years old" if age_days >= 365 else f"{age_days // 30} months old"
                children_desc.append(f"- Child {c['order']}: born {c['dob'].strftime('%d %b %Y')} ({age_str}), {c['citizenship']}")
            else:
                children_desc.append(f"- Child {c['order']}: date of birth not provided, {c['citizenship']}")
        children_text = "\n".join(children_desc)

        with st.spinner("Retrieving relevant information from RAG documents..."):
            query = f"Cash gifts grants benefits for family with children: {children_text}"
            relevant_docs = retriever.invoke(query)
            context = "\n\n".join([doc.page_content for doc in relevant_docs])

        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header">
            <span class="icon">📋</span>
            <h2>Cash Gifts & Grants</h2>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Analysing grants for your family..."):
            grants_prompt = f"""Based on the official government source data below, list ALL cash gifts and grants this family is eligible for from birth until each child turns 12 years old.

Family details:
{children_text}

Include all benefits across the child's life from age 0 to 12, such as:
- Baby Bonus Cash Gift (including instalment schedule if applicable)
- CDA First Step Grant
- CDA Government Co-Matching
- MediSave Grant for Newborns
- Child Development Credits
- Any other cash gifts, grants or credits the child receives up to age 12

Present the information as a markdown table with columns: Benefit Name, Child, Age/Stage When Received, Amount, Key Conditions.
After the table, show the estimated total cash gifts/grants per child and the family grand total.
Only include benefits the family is likely eligible for based on their children's details.
If a benefit eligibility is uncertain, note it clearly.

<context>
{context}
</context>"""

            grants_response = client.chat.completions.create(
                model=os.environ.get("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": grants_prompt}],
            )
            st.markdown(grants_response.choices[0].message.content)

        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

        earliest_dob = min(c["dob"] for c in children if c["dob"] is not None)
        latest_dob = max(c["dob"] for c in children if c["dob"] is not None)
        start_year = earliest_dob.year
        end_year = latest_dob.year + 12

        st.markdown("""
        <div class="section-header">
            <span class="icon">📅</span>
            <h2>Benefits Timeline (Birth to Age 12)</h2>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Generating year-by-year breakdown..."):
            timeline_prompt = f"""Based on the official government source data below, create a year-by-year breakdown of ALL cash gifts and grants this family receives from the 1st child's birth until the youngest child turns 12.

Family details:
{children_text}

Cover every year from {start_year} to {end_year}.

You MUST respond with ONLY a valid JSON array, no other text. Create a row for EACH child for EVERY year from that child's birth year until that child turns 12. Every child must appear in every year of their range, even if the amount is 0.

Each element should be an object with these exact keys:
- "Year": integer
- "Child": string (e.g. "Child 1", "Child 2")
- "Age": integer (child's age in that year, 0 for birth year)
- "Event": string (e.g. "Born", "Turns 6", "Baby Bonus instalment", or "-")
- "Cash Gift": integer (Baby Bonus Cash Gift dollar amount, 0 if none)
- "CDA First Step Grant": integer (one-time $5,000 at birth, 0 if none)
- "CDA Matching Cap": integer (government co-matching cap dollar amount, 0 if none)
- "MediSave Grant": integer (MediSave Grant for Newborns $4,000 at birth, 0 if none)
- "Edusave": integer (annual Edusave contributions, typically ages 6-16, 0 if none)
- "PSEA Top-Up": integer (Post-Secondary Education Account top-up, 0 if none)
- "Other Grants": integer (any other cash gifts or grants not covered above, 0 if none)

IMPORTANT: Every child MUST have exactly 13 rows (age 0 through age 12). Do NOT skip any year for any child even if all amounts are 0.

Rules:
- Cash gifts and grants triggered at birth — show them in the birth year (age 0).
- CDA First Step Grant is a one-time $5,000 grant deposited into the child's CDA at birth (for eligible Singapore Citizen children).
- MediSave Grant for Newborns is $4,000 deposited into the child's CPF MediSave account at birth.
- Baby Bonus Cash Gift is paid in instalments — distribute across the correct years based on the instalment schedule.
- Include any recurring annual grants or credits (e.g. Child Development Credits, Edusave) in the years they are received.
- If a benefit is paid in instalments, distribute across years.
- Use 0 for years with no benefit in that category — do NOT omit the row.

Respond with ONLY the JSON array, nothing else."""

            timeline_response = client.chat.completions.create(
                model=os.environ.get("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": timeline_prompt}],
            )

            import json as _json
            import pandas as pd

            raw = timeline_response.choices[0].message.content.strip()
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

            try:
                timeline_data = _json.loads(raw)
                df = pd.DataFrame(timeline_data)

                benefit_cols = ["Cash Gift", "CDA First Step Grant", "CDA Matching Cap", "MediSave Grant", "Edusave", "PSEA Top-Up", "Other Grants"]

                detail_display = df.copy()
                detail_display["Year Total"] = detail_display[benefit_cols].sum(axis=1)
                for col in benefit_cols + ["Year Total"]:
                    detail_display[col] = detail_display[col].apply(lambda x: f"${x:,}")
                st.dataframe(detail_display, use_container_width=True, hide_index=True)

                yearly = df.groupby("Year")[benefit_cols].sum().reset_index()

                cumulative = 0
                cumulative_col = []
                for _, row in yearly.iterrows():
                    cumulative += sum(row[col] for col in benefit_cols)
                    cumulative_col.append(cumulative)
                yearly["Cumulative Total"] = cumulative_col

                st.markdown("""
                <div class="section-header">
                    <span class="icon">📊</span>
                    <h2>Yearly Totals (All Children Combined)</h2>
                </div>
                """, unsafe_allow_html=True)
                yearly_display = yearly.copy()
                for col in benefit_cols + ["Cumulative Total"]:
                    yearly_display[col] = yearly_display[col].apply(lambda x: f"${x:,}")
                st.dataframe(yearly_display, use_container_width=True, hide_index=True)

                chart_df = yearly[["Year"] + benefit_cols].copy()
                chart_df = chart_df.set_index("Year")
                st.bar_chart(chart_df)

                st.markdown("""
                <div class="section-header">
                    <span class="icon">📈</span>
                    <h2>Cumulative Benefits Over Time</h2>
                </div>
                """, unsafe_allow_html=True)
                cumulative_df = yearly[["Year", "Cumulative Total"]].copy()
                cumulative_df = cumulative_df.set_index("Year")
                st.line_chart(cumulative_df)

            except (_json.JSONDecodeError, KeyError):
                st.markdown(timeline_response.choices[0].message.content)

        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="disclaimer-card">
            <p>⚠️ Information is retrieved from official government websites and summarised by AI.
            Amounts and eligibility may change — always verify with official sources before making financial decisions.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📚 Sources used"):
            for filename in filename_list:
                st.markdown(f"- {filename}")
