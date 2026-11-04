from django.urls import path
from .views import HomePage, QuizDetail

urlpatterns = [
    path("", HomePage.as_view(), name="index"),
    path("quiz/<int:pk>/", QuizDetail.as_view(), name="quiz")
]