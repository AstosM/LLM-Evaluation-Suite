from deepeval import assert_test
from deepeval.test_case import LLMTestCase

from evaluation.metrics import faithfulness_metric


def test_faithful_answer():
    test_case = LLMTestCase(
        input="What does faithfulness measure?",
        actual_output=(
            "Faithfulness measures whether an AI-generated answer "
            "is supported by the retrieved reference context."
        ),
        retrieval_context=[
            "Faithfulness measures whether an AI-generated answer "
            "is supported by the retrieved reference context. "
            "A faithful answer should not introduce unsupported facts."
        ]
    )

    assert_test(test_case, [faithfulness_metric])