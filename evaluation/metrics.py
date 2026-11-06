from deepeval.metrics import (
    FaithfulnessMetric,
    AnswerRelevancyMetric,
    HallucinationMetric
)
from deepeval.models import GeminiModel

from app.config import GOOGLE_API_KEY, GEMINI_MODEL_NAME


judge_model = GeminiModel(
    model=GEMINI_MODEL_NAME,
    api_key=GOOGLE_API_KEY
)


faithfulness_metric = FaithfulnessMetric(
    threshold=0.7,
    model=judge_model,
    include_reason=True
)

answer_relevancy_metric = AnswerRelevancyMetric(
    threshold=0.7,
    model=judge_model,
    include_reason=True
)

hallucination_metric = HallucinationMetric(
    threshold=0.7,
    model=judge_model,
    include_reason=True
)