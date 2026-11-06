import os
import sys
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from bs4 import BeautifulSoup
import requests
from openai import OpenAI

if not st.session_state.get("password_correct", False):
    st.warning("Please log in from the main page.")
    st.stop()


if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAPI_API_KEY"]

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

KB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "knowledge_base.json")

with open(KB_PATH, "r") as f:
    knowledge_base = json.load(f)

URLS = {entry["title"]: entry["url"] for entry in knowledge_base}

SYSTEM_PROMPT = """You are a helpful Singapore family benefits advisor. You answer questions based on official government source data provided below.

Rules:
- Present benefits in markdown tables where appropriate with columns like: Benefit Name, Eligibility Criteria, Benefit Amount, Additional Notes.
- If information is not available or uncertain, say so clearly.
- Only include benefits relevant to the user's question.
- Remember the conversation history and refer back to previous answers when the user asks follow-up questions.
- If the user asks to compare, elaborate, or drill into a previous answer, use the conversation context."""


@st.cache_data(ttl=3600)
def fetch_url_content(url):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)


@st.cache_data(ttl=3600)
def fetch_all_sources():
    all_text = {}
    for name, url in URLS.items():
        try:
            all_text[name] = fetch_url_content(url)
        except Exception:
            all_text[name] = ""
    context_parts = []
    for name, text in all_text.items():
        if text:
            context_parts.append(f"<source name=\"{name}\">\n{text[:5000]}\n</source>")
    return "\n\n".join(context_parts)


st.title("Ask me any question about Singapore family benefits")
st.caption("This page scrapes live content from all official government URLs listed in knowledge_base.json, sends the scraped text as context to OpenAI, and answers your questions. Supports follow-up questions with conversation history.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "context_loaded" not in st.session_state:
    st.session_state.context_loaded = False

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if question := st.chat_input("Ask about Singapore family benefits..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    if not st.session_state.context_loaded:
        with st.spinner("Fetching latest information from official government sources..."):
            st.session_state.context = fetch_all_sources()
            st.session_state.context_loaded = True

    system_message = SYSTEM_PROMPT + f"\n\n<context>\n{st.session_state.context}\n</context>"

    api_messages = [{"role": "system", "content": system_message}]
    for msg in st.session_state.messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=api_messages,
            )
            response = completion.choices[0].message.content
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar:
    st.subheader("Sources")
    for entry in knowledge_base:
        st.markdown(f"- [{entry['title']}]({entry['url']})")
    st.divider()
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()
    st.warning("Information is summarised by AI from official government websites. Always verify with official sources.")
