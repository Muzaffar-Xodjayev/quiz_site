from django.urls import path
from .views import SectionListAPIView, SectionQuestionsAPIView, QuizSubmitAPIView

urlpatterns = [
    path('sections/', SectionListAPIView.as_view()),
    path('sections/<int:section_id>/questions/', SectionQuestionsAPIView.as_view()),
    path('check_quiz/', QuizSubmitAPIView.as_view()),
]
