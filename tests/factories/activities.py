import factory
from apps.activities.models import Activity, Answer, Question


class ActivityFactory(factory.Factory):
    class Meta:
        model = Activity


class QuestionFactory(factory.Factory):
    question_text = "Quanto é 1+1?"

    class Meta:
        model = Question


class AnswerFactory(factory.Factory):
    answer_text = "2"
    is_correct = True
    # from_question = factory.SubFactory(QuestionFactory)
    from_question = None

    class Meta:
        model = Answer
