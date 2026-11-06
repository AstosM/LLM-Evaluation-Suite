from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.rag_pipeline import answer_question
from app.guardrails import validate_input, sanitize_output


app = FastAPI(
    title="LLM Evaluation & AI Safety Suite",
    description="LLM testing, evaluation and safety guardrails.",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    prompt: str
    response: str
    sources: list[str] = Field(default_factory=list)
    safety_findings: list[str] = Field(default_factory=list)


@app.get("/")
def home():
    return {"message": "LLM Evaluation Suite is running!"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    is_valid, message = validate_input(request.prompt)

    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail=message
        )

    try:
        result = answer_question(request.prompt)

        safe_answer, findings = sanitize_output(
            result["answer"]
        )

        return ChatResponse(
            prompt=request.prompt,
            response=safe_answer,
            sources=result["sources"],
            safety_findings=findings
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="LLM provider is temporarily unavailable."
        )