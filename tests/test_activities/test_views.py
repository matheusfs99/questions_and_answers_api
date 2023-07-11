from http import HTTPStatus
import uuid
import pytest
from pytest_factoryboy.fixture import register
from tests.factories.activities import ActivityFactory, AnswerFactory, QuestionFactory
from rest_framework.reverse import reverse
from apps.activities.models import Question, Answer

pytestmark = pytest.mark.django_db

register(ActivityFactory, "another_activity")
register(AnswerFactory, "another_answer")
register(QuestionFactory, "another_question")


def create_factory(factory, amount=1):
    for _ in range(amount):
        factory().save()


def test_list_activity(client, activity_factory):
    create_factory(activity_factory, 2)
    url = reverse("activity-list")
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 2


def test_create_activity(test_user, client):
    client.force_login(test_user)
    url = reverse("activity-list")
    response = client.post(url, {})
    assert response.status_code == HTTPStatus.CREATED


def test_create_activity_with_question(test_user, client, question_factory):
    create_factory(question_factory)
    question = Question.objects.all().first()
    client.force_login(test_user)
    url = reverse("activity-list")
    response = client.post(url, {"questions": [question.id]})
    assert response.status_code == HTTPStatus.CREATED
    assert len(response.json()["questions"]) > 0


def test_try_create_activity_unauthenticated(client):
    url = reverse("activity-list")
    response = client.post(url, {})
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_detail_activity(client, activity):
    activity.save()
    url = reverse("activity-detail", kwargs={"pk": activity.id})
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_detail_activity_nonexistent(client):
    url = reverse("activity-detail", kwargs={"pk": 123})
    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_activity(test_user, client, activity, question_factory):
    create_factory(question_factory)
    question = Question.objects.all().first()
    client.force_login(test_user)
    activity.save()
    url = reverse("activity-detail", kwargs={"pk": activity.id})
    payload = {
        "questions": [question.id]
    }
    response = client.put(url, payload, content_type="application/json")

    activity.refresh_from_db()

    assert response.status_code == HTTPStatus.OK
    assert str(activity.id) == response.json()["id"]
    assert [str(i.id) for i in activity.questions.all()] == response.json()["questions"]


def test_fail_update_evento(test_user, client, activity):
    client.force_login(test_user)
    activity.save()
    url = reverse("activity-detail", kwargs={"pk": activity.id})
    payload = {
        "questions": "question test",
    }
    response = client.put(url, payload, content_type="application/json")

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_try_update_activity_unauthenticated(test_user, client, activity):
    activity.save()
    url = reverse("activity-detail", kwargs={"pk": activity.id})
    payload = {
        "questions": [uuid.uuid4()],
    }
    response = client.put(url, payload, content_type="application/json")

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_list_questions(client, question_factory):
    create_factory(question_factory, 2)
    url = reverse("question-list")
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 2


def test_create_question(test_user, client):
    client.force_login(test_user)
    url = reverse("question-list")
    payload = {"question_text": "0 é número natural?"}
    response = client.post(url, payload)
    assert response.status_code == HTTPStatus.CREATED


def test_create_question_with_answer(test_user, client, answer_factory):
    create_factory(answer_factory)
    answer = Answer.objects.all().first()
    client.force_login(test_user)
    url = reverse("question-list")
    payload = {
        "question_text": "Quanto é 1 + 1?",
        "question_answers": [answer.id]
    }
    response = client.post(url, payload)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["question_answers"] is not None


def test_try_create_question_unauthenticated(client):
    url = reverse("question-list")
    payload = {"question_text": "0 é número natural?"}
    response = client.post(url, payload)
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_detail_question(client, question):
    question.save()
    url = reverse("question-detail", kwargs={"pk": question.id})
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_detail_question_nonexistent(client):
    url = reverse("question-detail", kwargs={"pk": 123})
    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_question(test_user, client, question):
    client.force_login(test_user)
    question.save()
    url = reverse("question-detail", kwargs={"pk": question.id})
    payload = {
        "question_text": "question updated",
    }
    response = client.put(url, payload, content_type="application/json")

    question.refresh_from_db()

    assert response.status_code == HTTPStatus.OK
    assert str(question.id) == response.json()["id"]
    assert response.json()["question_text"] == "question updated"


def test_fail_update_question(test_user, client, question):
    client.force_login(test_user)
    question.save()
    url = reverse("question-detail", kwargs={"pk": question.id})
    payload = {
        "question_answer": "question text test",
    }
    response = client.put(url, payload, content_type="application/json")

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_try_update_question_unauthenticated(test_user, client, question):
    question.save()
    url = reverse("question-detail", kwargs={"pk": question.id})
    payload = {
        "question_text": "aaaaaaaaa",
    }
    response = client.put(url, payload, content_type="application/json")

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_list_answers(client, answer_factory):
    create_factory(answer_factory, 2)
    url = reverse("answer-list")
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 2


def test_create_answer(test_user, client):
    client.force_login(test_user)
    url = reverse("answer-list")
    payload = {"answer_text": "response"}
    response = client.post(url, payload)
    assert response.status_code == HTTPStatus.CREATED


def test_create_answer_associated_a_question(test_user, client, question_factory):
    create_factory(question_factory)
    question = Question.objects.all().first()
    client.force_login(test_user)
    url = reverse("answer-list")
    payload = {
        "answer_text": "1",
        "is_correct": False,
        "from_question": question.id
    }
    response = client.post(url, payload)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["from_question"] is not None
    assert response.json()["from_question"] == str(question.id)


def test_try_create_answer_unauthenticated(client):
    url = reverse("answer-list")
    payload = {"answer_text": "response test"}
    response = client.post(url, payload)
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_detail_answer(client, answer):
    answer.save()
    url = reverse("answer-detail", kwargs={"pk": answer.id})
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_detail_answer_nonexistent(client):
    url = reverse("answer-detail", kwargs={"pk": 123})
    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_answer(test_user, client, answer):
    client.force_login(test_user)
    answer.save()
    url = reverse("answer-detail", kwargs={"pk": answer.id})
    payload = {
        "answer_text": "answer updated",
    }
    response = client.put(url, payload, content_type="application/json")

    answer.refresh_from_db()

    assert response.status_code == HTTPStatus.OK
    assert str(answer.id) == response.json()["id"]
    assert response.json()["answer_text"] == "answer updated"


def test_fail_update_answer(test_user, client, answer):
    client.force_login(test_user)
    answer.save()
    url = reverse("answer-detail", kwargs={"pk": answer.id})
    payload = {
        "from_question": "question test",
    }
    response = client.put(url, payload, content_type="application/json")

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_try_update_answer_unauthenticated(test_user, client, answer):
    answer.save()
    url = reverse("answer-detail", kwargs={"pk": answer.id})
    payload = {
        "answer_text": "aaaaaaaaa",
    }
    response = client.put(url, payload, content_type="application/json")

    assert response.status_code == HTTPStatus.FORBIDDEN
