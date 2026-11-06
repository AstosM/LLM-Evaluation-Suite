from deepeval import assert_test
from deepeval.test_case import LLMTestCase

from evaluation.metrics import hallucination_metric


def test_answer_without_hallucination():
    test_case = LLMTestCase(
        input="What is RAG?",
        actual_output=(
            "RAG combines information retrieval with language generation. "
            "It retrieves relevant documents and provides them as context "
            "to the language model."
        ),
        context=[
            "Retrieval-Augmented Generation combines information retrieval "
            "with language generation. The system searches a knowledge base "
            "and provides retrieved information as context to the language model."
        ]
    )

    assert_test(test_case, [hallucination_metric])