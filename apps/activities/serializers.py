from rest_framework import serializers
from .models import Activity, Answer, Question


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ("id", "questions")
        extra_kwargs = {"created_by": {"default": serializers.CurrentUserDefault()}}


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "answer_text", "is_correct", "from_question")


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "question_text", "question_answers")
