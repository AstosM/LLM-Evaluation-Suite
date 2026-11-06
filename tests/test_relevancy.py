from deepeval import assert_test
from deepeval.test_case import LLMTestCase

from evaluation.metrics import answer_relevancy_metric


def test_relevant_answer():
    test_case = LLMTestCase(
        input="What is ChromaDB?",
        actual_output=(
            "ChromaDB is a vector database used to store and retrieve "
            "document embeddings through similarity search."
        )
    )

    assert_test(test_case, [answer_relevancy_metric])