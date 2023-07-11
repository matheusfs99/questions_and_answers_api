import pytest


@pytest.fixture
def question_payload(question, answer_payload):
    return {
        "id": question.id,
        "question_text": question.question_text,
        "question_answers": [],
    }


@pytest.fixture
def answer_payload(answer):
    return {
        "id": answer.id,
        "answer_text": answer.answer_text,
        "is_correct": answer.is_correct,
        "from_question": None,
    }
