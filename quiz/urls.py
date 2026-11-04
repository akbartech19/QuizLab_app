
from django.urls import path
from . import views

urlpatterns = [
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("start/<int:quiz_id>/", views.start_quiz, name="start_quiz"),
    path("take/<int:quiz_id>/", views.take_quiz, name="take_quiz"),
]

