from django.contrib.auth.models import User
from pytest_factoryboy import register
from tests.factories.activities import ActivityFactory, AnswerFactory, QuestionFactory
import pytest

register(ActivityFactory)
register(AnswerFactory)
register(QuestionFactory)


@pytest.fixture
def test_user():
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()
    return user
