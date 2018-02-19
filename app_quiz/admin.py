from django.contrib import admin
from .models import Quiz, Question, MultipleChoice, TextAnswer, Submission


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 5


class MultipleChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'isCorrectAnswer')


class TextAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'correctAnswer')


class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'pub_date')
    inlines = [QuestionInline]


class SubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ('pub_date', 'hash_id')
    list_display = ('id', 'quiz', 'pub_date', 'hash_id')

admin.site.register(Quiz, QuizAdmin)
admin.site.register(MultipleChoice, MultipleChoiceAdmin)
admin.site.register(TextAnswer, TextAnswerAdmin)
admin.site.register(Submission, SubmissionAdmin)
