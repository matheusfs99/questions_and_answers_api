from uuid import UUID


def test_simple_activity(activity):
    assert activity
    assert isinstance(activity.id, UUID)


def test_simple_question(question):
    assert question
    assert isinstance(question.id, UUID)


def test_simple_answer(answer):
    assert answer
    assert isinstance(answer.id, UUID)
