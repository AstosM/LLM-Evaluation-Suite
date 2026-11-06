# Automated LLM Evaluation & AI Safety Guardrail Suite

An automated testing and evaluation framework for a Retrieval-Augmented Generation (RAG) application. It combines Google Gemini-powered answer generation, ChromaDB-based document retrieval, DeepEval evaluation metrics, and Python-based safety guardrails to assess LLM response quality and detect common security risks.

## Key Features

- **RAG Pipeline:** Retrieves relevant knowledge-base chunks using ChromaDB and generates context-grounded answers using Gemini.
- **LLM Evaluation:** Uses DeepEval to evaluate Faithfulness, Answer Relevancy, and Hallucination.
- **Prompt Injection Detection:** Uses regex-based input validation to identify known prompt-injection patterns.
- **PII Protection:** Detects and redacts email addresses, phone numbers, Aadhaar-like numbers, and Google API key patterns in generated responses.
- **Automated Testing:** Uses Pytest for functional, safety, and LLM evaluation tests.
- **Golden Dataset Benchmarking:** Measures response latency and expected-keyword coverage.
- **Run Comparison:** Compares benchmark runs to identify latency changes, keyword-score differences, and response variations.
- **JSON Reports:** Generates timestamped benchmark reports for later analysis.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python 3.11 |
| Backend API | FastAPI |
| LLM Provider | Google Gemini |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| LLM Evaluation | DeepEval |
| Testing Framework | Pytest |
| Data Storage | JSON |

## Project Architecture

```text
llm-evaluation-suite/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── chatbot.py
│   ├── rag_pipeline.py
│   ├── retriever.py
│   └── guardrails.py
│
├── evaluation/
│   ├── __init__.py
│   ├── metrics.py
│   ├── evaluator.py
│   └── safety_evaluator.py
│
├── tests/
│   ├── __init__.py
│   ├── test_faithfulness.py
│   ├── test_relevancy.py
│   ├── test_hallucination.py
│   ├── test_prompt_injection.py
│   └── test_pii_leakage.py
│
├── datasets/
│   ├── golden_dataset.json
│   ├── adversarial_prompts.json
│   └── knowledge_base.txt
│
├── reports/
│
├── scripts/
│   ├── ingest_documents.py
│   ├── run_benchmark.py
│   └── compare_runs.py
│
├── requirements.txt
├── pytest.ini
├── .env.example
├── .gitignore
└── README.md
```

## System Workflow

1. **Document Ingestion:** Reads knowledge-base documents and divides them into smaller, overlapping text chunks.
2. **Embedding Generation:** Sentence Transformers converts the chunks into numerical embeddings.
3. **Vector Storage:** ChromaDB stores the embeddings and retrieves relevant chunks using similarity search.
4. **Context Construction:** The RAG pipeline combines retrieved information with the user's question.
5. **Answer Generation:** Gemini generates an answer using the retrieved context.
6. **Output Safety:** Guardrails scan generated responses and redact supported PII patterns.
7. **LLM Evaluation:** DeepEval evaluates answer quality using predefined evaluation metrics.
8. **Automated Testing:** Pytest executes functional, prompt-injection, PII, and LLM evaluation tests.
9. **Benchmark Analysis:** Benchmark scripts record latency, keyword coverage, and response variations across multiple runs.

## LLM Evaluation Metrics

The project integrates three DeepEval metrics:

| Metric | Purpose |
|---|---|
| Faithfulness | Checks whether the generated answer is supported by the retrieved context. |
| Answer Relevancy | Measures how relevant the generated answer is to the original question. |
| Hallucination | Evaluates whether the answer contains information unsupported by the provided context. |

**Evaluation Threshold:** Each metric is configured with a threshold of `0.7`.

## AI Safety Testing

The safety testing suite currently covers:

- 25 adversarial prompt-injection test cases.
- Empty-input validation.
- Oversized-input validation.
- Email address detection and redaction.
- Phone number detection and redaction.
- Aadhaar-like number detection and redaction.
- Google API key pattern detection and redaction.
- Safe-output preservation tests.

**Security Note:** The current guardrails use regular expressions to detect predefined patterns. They provide baseline protection but are not a comprehensive defense against all prompt-injection, adversarial, or data-leakage attacks.

## Golden Dataset Benchmarking

The project uses a golden dataset containing three predefined questions.

For each question, the benchmark records:

- Generated answer.
- Retrieved source information.
- Response latency in seconds.
- Expected-keyword coverage score.
- Matched expected keywords.

Each benchmark execution generates a timestamped JSON report inside the `reports/` directory.

### Benchmark Comparison

The comparison script analyzes the latest two benchmark reports and checks:

- Response latency changes.
- Expected-keyword coverage differences.
- Whether the generated answer text changed between runs.

**Important:** A changed answer does not necessarily indicate factual drift. Similarly, keyword coverage is a simple text-overlap measure and is not a substitute for semantic or factual evaluation.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/AstosM/LLM-Evaluation-Suite.git
cd LLM-Evaluation-Suite
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it using Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a template.

Add your own Gemini API key:

```env
GOOGLE_API_KEY=your_gemini_api_key
GEMINI_MODEL_NAME=gemini-3.5-flash-lite
USE_GEMINI_MODEL=1
```

Never commit your `.env` file or expose your API key publicly.

### 5. Ingest the knowledge base

```bash
python scripts/ingest_documents.py
```

This processes the knowledge-base document and stores its embeddings in ChromaDB.

### 6. Start the FastAPI application

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

Use the `/chat` endpoint to submit questions to the RAG application.

## Running Tests

### Run safety tests

```bash
python -m pytest tests/test_prompt_injection.py tests/test_pii_leakage.py -q --tb=short
```

### Run individual DeepEval tests

```bash
python -m pytest tests/test_faithfulness.py -q --tb=short

python -m pytest tests/test_relevancy.py -q --tb=short

python -m pytest tests/test_hallucination.py -q --tb=short
```

**Note:** DeepEval tests make external model calls and may take longer or fail temporarily due to provider availability or API limits.

## Running Benchmarks

Execute the benchmark:

```bash
python scripts/run_benchmark.py
```

Run it again to generate another benchmark report.

Compare the latest two reports:

```bash
python scripts/compare_runs.py
```

The comparison output helps analyze changes in response latency, keyword coverage, and generated answer text.

## Verified Development Results

The following results were obtained during project development:

| Test Area | Verified Result |
|---|---:|
| Adversarial prompt-injection cases | 25 passed |
| Additional input-validation tests | 3 passed |
| PII redaction tests | 5 passed |
| Combined safety test suite | 33 passed |
| DeepEval Faithfulness | Passed individually |
| DeepEval Answer Relevancy | Passed individually |
| DeepEval Hallucination | Passed individually |
| Golden dataset benchmark | 3 successful cases in each of 2 runs |

These are development-time results, not guarantees of production-level security or model reliability.

## Limitations and Future Improvements

- Expand the golden dataset with more diverse questions.
- Introduce semantic evaluation alongside keyword coverage.
- Improve prompt-injection detection beyond regex-based patterns.
- Expand automated safety evaluation with more adversarial scenarios.
- Track evaluation metrics across larger benchmark runs.
- Add CI workflows to execute tests automatically after code changes.
- Improve reporting with visual summaries and performance trends.

## Author

**Ashutosh Maurya**

B.Tech – Information Technology

GitHub: [AstosM](https://github.com/AstosM)

**Repository:** [LLM Evaluation & AI Safety Guardrail Suite](https://github.com/AstosM/LLM-Evaluation-Suite)
