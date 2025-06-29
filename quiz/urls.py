from django.urls import path
from .views import SectionListAPIView


urlpatterns = [
    path('sections/', SectionListAPIView.as_view()),
]
