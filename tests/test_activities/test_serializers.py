import pytest
from apps.activities.serializers import ActivitySerializer, AnswerSerializer, QuestionSerializer

pytestmark = pytest.mark.django_db


def test_create_activity_serializer_data(activity):
    serializer = ActivitySerializer(instance=activity)
    assert serializer.data == {
        "id": str(activity.id),
        "questions": [],
    }


def test_create_activity_serializer():
    serializer = ActivitySerializer(data={})
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    activity = serializer.create(validated_data)

    assert activity.id


def test_partial_update_activity_serializer(activity, question):
    old_questions = activity.questions.all()
    serializer = QuestionSerializer(
        instance=activity, data={"questions": [question]}, partial=True
    )
    serializer.is_valid(raise_exception=True)
    updated_activity = serializer.save()

    assert updated_activity.id == activity.id
    assert updated_activity.questions.all() != old_questions


def test_create_question_serializer_data(question):
    serializer = QuestionSerializer(instance=question)
    assert serializer.data == {
        "id": str(question.id),
        "question_text": question.question_text,
        "question_answers": [],
    }


def test_create_question_serializer(question_payload):
    serializer = QuestionSerializer(data=question_payload)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    question = serializer.create(validated_data)

    assert question.id


def test_create_question_without_field_data(question_payload):
    question_payload.pop("question_text")
    serializer = QuestionSerializer(data=question_payload)
    assert not serializer.is_valid()


def test_create_question_with_field_blank(question_payload):
    question_payload["question_text"] = ""
    serializer = QuestionSerializer(data=question_payload)
    assert not serializer.is_valid()


def test_partial_update_question_serializer(question):
    old_question_text = question.question_text
    serializer = QuestionSerializer(
        instance=question, data={"question_text": "Quanto é 2+2?"}, partial=True
    )
    serializer.is_valid(raise_exception=True)
    updated_question = serializer.save()

    assert updated_question.id == question.id
    assert updated_question.question_text != old_question_text


def test_create_answer_serializer_data(answer):
    serializer = AnswerSerializer(instance=answer)
    assert serializer.data == {
        "id": str(answer.id),
        "answer_text": answer.answer_text,
        "is_correct": answer.is_correct,
        "from_question": None,
    }


def test_create_answer_serializer(answer_payload):
    serializer = AnswerSerializer(data=answer_payload)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    answer = serializer.create(validated_data)

    assert answer.id


def test_create_answer_without_field_data(answer_payload):
    answer_payload.pop("answer_text")
    serializer = AnswerSerializer(data=answer_payload)
    assert not serializer.is_valid()


def test_create_answer_with_field_blank(answer_payload):
    answer_payload["answer_text"] = ""
    serializer = AnswerSerializer(data=answer_payload)
    assert not serializer.is_valid()


def test_partial_update_answer_serializer(answer):
    answer.from_question = None
    old_answer_text = answer.answer_text
    serializer = AnswerSerializer(
        instance=answer, data={"answer_text": "new answer"}, partial=True
    )
    serializer.is_valid(raise_exception=True)
    updated_answer = serializer.save()

    assert updated_answer.id == answer.id
    assert updated_answer.answer_text != old_answer_text
