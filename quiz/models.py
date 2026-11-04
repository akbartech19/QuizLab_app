from django.db import models
from django.contrib.auth.models import User


class Science(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=20)
    status = models.BooleanField(default=True)

    science = models.ForeignKey(
        Science,
        on_delete=models.CASCADE,
        related_name="quizzes"
    )

    def __str__(self):
        return self.title

class Question(models.Model):
    question_text = models.TextField()

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    def __str__(self):
        return self.question_text[:60]


class QuestionVariant(models.Model):
    variant_text = models.CharField(max_length=255)

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.variant_text


class Answer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="quiz_answers"
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="user_answers"
    )

    correct_answers = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"