from django.db import models
from apps.base.models import BaseModel


class Answer(BaseModel):
    answer_text = models.TextField(max_length=255)
    is_correct = models.BooleanField(default=False)
    from_question = models.ForeignKey("Question", related_name="answers", null=True, on_delete=models.CASCADE)

    def __str__(self):
        if len(str(self.answer_text)) < 15:
            return self.answer_text
        return self.answer_text[:15] + "..."

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        question = Question.objects.get(pk=self.from_question.id)
        question.question_answers.add(self.pk)
        question.save()


class Question(BaseModel):
    question_text = models.TextField()
    question_answers = models.ManyToManyField("Answer", related_name="question", null=True, blank=True)

    def __str__(self):
        if len(str(self.question_text)) < 15:
            return self.question_text
        return self.question_text[:15] + "..."


class Activity(BaseModel):
    questions = models.ManyToManyField("Question", null=True, blank=True)

    def __str__(self):
        return f"Atividade {self.pk}"
