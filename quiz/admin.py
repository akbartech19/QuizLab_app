from django.contrib import admin
from .models import Science, Quiz, Question, QuestionVariant, Answer

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    fields = ("question_text",)
    show_change_link = True


class QuestionVariantInline(admin.TabularInline):
    model = QuestionVariant
    extra = 4
    fields = ("variant_text", "is_correct")


@admin.register(Science)
class ScienceAdmin(admin.ModelAdmin):
    list_display = ("name", "date_created")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "science",
        "start_time",
        "end_time",
        "duration_minutes",
        "status",
    )

    list_filter = ("science", "status")
    search_fields = ("title", "science__name")
    ordering = ("-date_created",)

    fieldsets = (
        ("Quiz information", {"fields": ("title", "science", "status")}),
        ("Quiz schedule", {"fields": ("start_time", "end_time")}),
    )

    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("short_question", "quiz")
    list_filter = ("quiz",)
    search_fields = ("question_text", "quiz__title")
    inlines = [QuestionVariantInline]

    @admin.display(description="Question")
    def short_question(self, obj):
        return obj.question_text[:60]


@admin.register(QuestionVariant)
class QuestionVariantAdmin(admin.ModelAdmin):
    list_display = ("variant_text", "question", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("variant_text", "question__question_text")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "correct_answers")
    list_filter = ("quiz",)
    search_fields = ("user__username", "quiz__title")