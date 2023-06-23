from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, AnswerViewSet, QuestionViewSet


router = DefaultRouter()
router.register("activity", ActivityViewSet, basename="activity")
router.register("answer", AnswerViewSet, basename="answer")
router.register("question", QuestionViewSet, basename="question")
urlpatterns = [
    path("", include(router.urls))
]
