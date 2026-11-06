# Automated LLM Evaluation \& AI Safety Guardrail Suite



An automated testing and evaluation framework for a Retrieval-Augmented Generation (RAG) application. It combines Gemini-powered answer generation, ChromaDB-based document retrieval, DeepEval metrics, and Python safety guardrails to evaluate LLM response quality and detect common security risks.



## Features



- \*\*RAG Pipeline:\*\* Retrieves relevant knowledge-base chunks using ChromaDB and generates context-grounded answers with Gemini.

- \*\*LLM Evaluation:\*\* Uses DeepEval to evaluate Faithfulness, Answer Relevancy, and Hallucination.

- \*\*Prompt Injection Detection:\*\* Uses regex-based input validation to detect known prompt-injection patterns.

- \*\*PII Protection:\*\* Detects and redacts email addresses, phone numbers, Aadhaar-like numbers, and Google API key patterns in generated responses.

- \*\*Automated Testing:\*\* Uses Pytest to run functional, safety, and evaluation tests.

- \*\*Golden Dataset Benchmarking:\*\* Measures response latency and expected-keyword coverage.

- \*\*Run Comparison:\*\* Compares benchmark reports to identify latency changes and response variations.

- \*\*JSON Reports:\*\* Stores benchmark results for later analysis.



## Technology Stack



| Category | Technologies |

|---|---|

| Language | Python 3.11 |

| API | FastAPI |

| LLM | Google Gemini |

| Vector Database | ChromaDB |

| Embeddings | Sentence Transformers |

| Evaluation | DeepEval |

| Testing | Pytest |

| Data Format | JSON |



## Project Architecture



```text

llm-evaluation-suite/

│

├── app/

│   ├── config.py

│   ├── main.py

│   ├── chatbot.py

│   ├── rag\_pipeline.py

│   ├── retriever.py

│   └── guardrails.py

│

├── evaluation/

│   ├── metrics.py

│   └── evaluator.py

│

├── tests/

│   ├── test\_faithfulness.py

│   ├── test\_relevancy.py

│   ├── test\_hallucination.py

│   ├── test\_prompt\_injection.py

│   └── test\_pii\_leakage.py

│

├── datasets/

│   ├── golden\_dataset.json

│   ├── adversarial\_prompts.json

│   └── knowledge\_base.txt

│

├── scripts/

│   ├── ingest\_documents.py

│   ├── run\_benchmark.py

│   └── compare\_runs.py

│

├── reports/

├── requirements.txt

├── pytest.ini

├── .env.example

├── .gitignore

└── README.md

```



## How It Works



1\. Documents are split into smaller overlapping chunks.

2\. Sentence Transformers converts the chunks into embeddings.

3\. ChromaDB stores the embeddings and retrieves relevant chunks for a user query.

4\. The RAG pipeline combines retrieved context with the user's question.

5\. Gemini generates an answer using the supplied context.

6\. Output guardrails scan the generated response and redact supported PII patterns.

7\. DeepEval evaluates answer quality using predefined metrics.

8\. Pytest runs automated functional and safety tests.

9\. The benchmark scripts measure latency, keyword coverage, and response variation across runs.



## Evaluation Metrics



The project uses three DeepEval metrics:



- \*\*Faithfulness:\*\* Checks whether the generated answer is supported by the retrieved context.

- \*\*Answer Relevancy:\*\* Measures how relevant the answer is to the user's question.

- \*\*Hallucination:\*\* Evaluates whether the answer contains information unsupported by the provided context.



Each metric uses a configured threshold of 0.7.



## Safety Testing



The safety test suite currently includes:



- 25 adversarial prompt-injection test cases.

- Empty-input validation.

- Oversized-input validation.

- PII redaction tests for email, phone, Aadhaar-like numbers, and API-key patterns.



The current guardrails use regular expressions and provide baseline protection against known patterns. They are not a comprehensive defense against all prompt-injection or data-leakage attacks.



## Benchmarking



A golden dataset contains three questions used to benchmark the RAG application.



The benchmark records:



\- Response latency in seconds.

\- Expected-keyword coverage score.

\- Retrieved source information.

\- Generated answers.



Each run generates a timestamped JSON report inside the `reports/` directory.



The comparison script checks latency changes, keyword scores, and whether generated answers changed between two runs.



\*\*Note:\*\* Keyword coverage is a simple text-overlap measure, not a substitute for semantic or factual evaluation.



\## Installation and Setup



\### 1. Clone the repository



```bash

git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

cd llm-evaluation-suite

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



Activate it on Windows PowerShell:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\### 3. Install dependencies



```bash

pip install -r requirements.txt

```



\### 4. Configure environment variables



Create a `.env` file in the project root and add:



```env

GOOGLE\_API\_KEY=your\_gemini\_api\_key

GEMINI\_MODEL\_NAME=your\_supported\_gemini\_model

USE\_GEMINI\_MODEL=1

```



Never commit your `.env` file or expose your API key.



\### 5. Ingest the knowledge base



```bash

python scripts/ingest\_documents.py

```



\### 6. Start the API



```bash

uvicorn app.main:app --reload

```



Open the interactive API documentation:



```text

http://127.0.0.1:8000/docs

```



Use the `/chat` endpoint to submit questions.



\## Running Tests



Run the safety tests:



```bash

python -m pytest tests/test\_prompt\_injection.py tests/test\_pii\_leakage.py -q

```



Run individual LLM evaluation tests:



```bash

python -m pytest tests/test\_faithfulness.py -q

python -m pytest tests/test\_relevancy.py -q

python -m pytest tests/test\_hallucination.py -q

```



DeepEval tests make external model calls and may take longer or fail temporarily if the provider is unavailable.



\## Running Benchmarks



Run the benchmark:



```bash

python scripts/run\_benchmark.py

```



Run it again to generate another report, then compare the latest two reports:



```bash

python scripts/compare\_runs.py

```



\## Current Test Results



Verified during development:



| Test Area | Result |

|---|---:|

| Adversarial prompt-injection cases | 25 passed |

| Additional input-validation tests | 3 passed |

| PII redaction tests | 5 passed |

| Combined safety tests | 33 passed |

| DeepEval Faithfulness | Passed individually |

| DeepEval Answer Relevancy | Passed individually |

| DeepEval Hallucination | Passed individually |

| Golden dataset benchmark | 3 successful cases in each of 2 runs |



These are development test results, not a guarantee of production-level security or model reliability.



\## Limitations and Future Improvements



\- Expand the golden dataset with more diverse questions.

\- Add semantic evaluation to complement keyword coverage.

\- Improve prompt-injection detection beyond regex patterns.

\- Add automated evaluation of safety behavior and response consistency.

\- Track evaluation metrics across larger benchmark runs.

\- Add CI workflows to run tests automatically on code changes.

\- Improve reporting with visual summaries and trend analysis.



\## Author



\*\*Ashutosh Maurya\*\*



B.Tech – Information Technology



