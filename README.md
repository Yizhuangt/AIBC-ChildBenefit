
# Singapore Family Benefits Advisor — lightweight RAG

A Streamlit assessment project demonstrating Retrieval-Augmented Generation (RAG) for Singapore family-support schemes. It is a **research prototype**, not an official government service or a certified entitlement calculator.

## Features

- **Benefits Advisor:** retrieves relevant source records and produces a grounded answer when an OpenAI key is configured.
- **Benefit Explorer:** browse a starter catalogue by category and verification status.
- **Timeline Calculator worksheet:** collect children's DOB/citizenship for planning; it deliberately avoids making unverified payout calculations.
- **RAG Explorer:** inspect retrieved records and scores for an assessment/demo.
- **Fallback mode:** without an API key, the app uses simple keyword matching and displays retrieved evidence.
- **Date-aware research design:** the starter data marks historical rules as needing verification rather than inferring old rules from today's scheme.

## Quick start

Requires Python 3.10+ (Python 3.11 recommended).

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1

pip install -r requirements.txt
cp .env.example .env
# Edit .env and set OPENAI_API_KEY if you want LLM answers and embeddings.
streamlit run app.py
```

No API key? The app still starts in demo mode and retrieves by keyword. With a key, it uses OpenAI embeddings and a chat model. API usage may incur charges.

## Project structure

```text
app.py
src/
  data.py
  rag_engine.py
data/
  benefits.json
  knowledge_base.json
tests/
  test_rag_engine.py
.env.example
requirements.txt
```

## How the RAG pipeline works

1. **Knowledge source:** `data/knowledge_base.json` contains source metadata and short excerpts.
2. **Retrieval:** with `OPENAI_API_KEY`, `src/rag_engine.py` embeds the query and source excerpts and ranks them with cosine similarity (NumPy). Without a key, it uses transparent keyword overlap.
3. **Augmentation:** the top retrieved records and their URLs are added to the model prompt.
4. **Generation:** the model is instructed to answer only from supplied evidence, cite sources using `[1]`, `[2]`, and state uncertainty when evidence is insufficient.
5. **Inspection:** RAG Explorer displays the selected records and relevance scores.

This starter version embeds the small source catalogue at query time for simplicity. For a larger collection, precompute embeddings and persist a vector index. Add an ingestion pipeline for official HTML/PDF files and preserve publication date, effective period, section/page, retrieval date, and verification status.

## Adding knowledge

Add an object to `data/knowledge_base.json` with these fields:

```json
{
  "id": "unique-id",
  "title": "Scheme or document title",
  "agency": "Official agency",
  "category": "Category",
  "effective_period": "Period supported by this source",
  "status": "Verified | Partially verified | Needs verification | Announced / future | Superseded",
  "url": "https://official.gov.sg/page",
  "tags": "search terms",
  "excerpt": "Short evidence excerpt or a carefully prepared summary"
}
```

Use official government sources as the primary authority. The current seed records are **source discovery leads**, not a verified complete historical dataset. Do not label an amount or historical rule as verified unless the underlying official document supports it.

## Next steps for the assessment

1. Collect 10–20 official HTML pages/PDFs and save provenance metadata.
2. Add document loading and chunking; preserve source URL and section/page references.
3. Build a versioned structured schema for schemes and rules (effective start/end dates).
4. Implement deterministic eligibility/calculation functions only for rules that have been verified.
5. Create a small evaluation set: question, expected evidence/source, expected answer points.
6. Evaluate retrieval relevance, citation coverage, and whether unsupported questions trigger uncertainty.
7. Add tests for date boundaries and ensure tax relief, cash grants, subsidies, savings, and leave are shown as different benefit types.

## Security and privacy

- Keep `.env` out of source control.
- Never expose the API key in the Streamlit interface.
- Avoid collecting names, NRICs, or personal information not required for a scheme.
- The current DOB worksheet keeps values in the Streamlit session and does not submit them to the LLM.
- Confirm all benefit rules and claims with the relevant government agency.
