
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from quiz.models import Answer
from django.db.models import Sum


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            user.first_name = request.POST.get("first_name", "")
            user.last_name = request.POST.get("last_name", "")
            user.email = request.POST.get("email", "")
            user.save()

            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Username yoki parol noto'g'ri.")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)

    return redirect("index")


from quiz.models import Answer


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    recent_results = Answer.objects.filter(
        user=request.user
    ).select_related("quiz").order_by("-id")[:5]

    password_form = PasswordChangeForm(user=request.user)

    return render(request, "profile.html", {
        "user": request.user,
        "profile": profile,
        "recent_results": recent_results,
        "password_form": password_form,
    })


@login_required
def profile_update(request):
    if request.method == "POST":
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)

        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")
        user.email = request.POST.get("email", "")
        profile.about = request.POST.get("bio", "")

        if request.FILES.get("photo"):
            profile.profile_image = request.FILES["photo"]

        user.save()
        profile.save()

        messages.success(request, "Profile updated successfully!")

    return redirect("profile")


@login_required
def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(
                request,
                "Password changed successfully!"
            )
        else:
            messages.error(
                request,
                "Password could not be changed. Check the fields."
            )

    return redirect("profile")

def user_profile(request, user_id):
    person = get_object_or_404(User, id=user_id)

    print("USER ID:", person.id)
    print("USERNAME:", person.username)

    profile = Profile.objects.filter(user=person).first()

    answers = Answer.objects.filter(user=person)

    results = answers.select_related("quiz").order_by("-id")[:5]

    solved_count = answers.count()

    total_score = answers.aggregate(
        total=Sum("correct_answers")
    )["total"] or 0

    return render(request, "user_profile.html", {
        "person": person,
        "profile": profile,
        "results": results,
        "solved_count": solved_count,
        "total_score": total_score,
    })