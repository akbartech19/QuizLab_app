from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from .models import Answer, Quiz, Question, QuestionVariant
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required



def leaderboard(request):
    users = User.objects.annotate(
        total_score=Sum("quiz_answers__correct_answers")
    ).order_by("-total_score", "username")

    search = request.GET.get("search", "").strip()

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )

    top_users = list(users[:3])

    return render(
        request,
        "leaderboard.html",
        {
            "users": users,
            "top_users": top_users,
            "search": search,
        }
    )



def user_profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)

    answers = Answer.objects.filter(
        user=profile_user
    ).select_related("quiz").order_by("-id")

    total_solved = answers.count()

    total_correct = 0
    for answer in answers:
        total_correct += answer.correct_answers

    average = 0
    if total_solved > 0:
        average = round(total_correct / total_solved, 1)

    return render(
        request,
        "user_profile.html",
        {
            "profile_user": profile_user,
            "answers": answers[:5],
            "total_solved": total_solved,
            "average": average,
        }
    )

@login_required
@require_POST
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, status=True)
    now = timezone.now()

    if now < quiz.start_time:
        return render(request, "quiz/unavailable.html", {
            "message": "This quiz has not started yet."
        })

    if now >= quiz.end_time:
        return render(request, "quiz/unavailable.html", {
            "message": "This quiz has already ended."
        })

    # Har bir foydalanuvchi uchun quiz boshlanish vaqtini saqlaymiz.
    deadline = now + timezone.timedelta(minutes=quiz.duration_minutes)

    # Quizning umumiy tugash vaqtidan oshib ketmasin.
    if deadline > quiz.end_time:
        deadline = quiz.end_time

    request.session[f"quiz_{quiz.id}_deadline"] = deadline.isoformat()

    return redirect("take_quiz", quiz_id=quiz.id)


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, status=True)

    deadline_value = request.session.get(f"quiz_{quiz.id}_deadline")

    if not deadline_value:
        return redirect("index")

    deadline = timezone.datetime.fromisoformat(deadline_value)
    now = timezone.now()

    questions = Question.objects.filter(quiz=quiz).prefetch_related("variants")

    if request.method == "POST":
        if now >= deadline:
            return render(request, "quiz/take_quiz.html", {
                "quiz": quiz,
                "questions": questions,
                "expired": True,
            })

        correct_count = 0

        for question in questions:
            selected_variant_id = request.POST.get(f"question_{question.id}")

            if selected_variant_id:
                variant = QuestionVariant.objects.filter(
                    id=selected_variant_id,
                    question=question,
                    is_correct=True
                ).first()

                if variant:
                    correct_count += 1

        Answer.objects.create(
            user=request.user,
            quiz=quiz,
            correct_answers=correct_count
        )

        del request.session[f"quiz_{quiz.id}_deadline"]

        return render(request, "quiz/take_quiz.html", {
            "quiz": quiz,
            "result": True,
            "correct_count": correct_count,
            "total_questions": questions.count(),
        })

    return render(request, "quiz/take_quiz.html", {
        "quiz": quiz,
        "questions": questions,
        "deadline_ms": int(deadline.timestamp() * 1000),
    })