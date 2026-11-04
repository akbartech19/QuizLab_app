from django.views.generic import ListView, DetailView
from django.utils import timezone
from quiz.models import Quiz, Science
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView
from django.utils import timezone
from quiz.models import Quiz, Science


class HomePage(ListView):
    model = Quiz
    template_name = "index.html"
    context_object_name = "upcoming_quizzes"
    paginate_by = 10

    def get_queryset(self):
        data = super().get_queryset()

        title = self.request.GET.get("title")
        science = self.request.GET.get("science")

        if title:
            data = data.filter(title__icontains=title)

        if science:
            data = data.filter(science__name__icontains=science)

        return data.order_by("-date_created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sciences"] = Science.objects.all()
        context["now"] = timezone.now()
        return context
    template_name = "index.html"
    context_object_name = "upcoming_quizzes"
    model = Quiz
    paginate_by = 10

    def get_queryset(self):
        data = super().get_queryset()

        title = self.request.GET.get("title")
        science = self.request.GET.get("science")

        if title:
            data = data.filter(title__icontains=title)

        if science:
            data = data.filter(science__name__icontains=science)

        return data.order_by("-date_created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sciences"] = Science.objects.all()
        context["now"] = timezone.now()

        print("SCIENCES:", list(context["sciences"].values("id", "name")))

        return context
    
class QuizDetail(LoginRequiredMixin, DetailView):
    template_name = "quiz.html"
    model= Quiz