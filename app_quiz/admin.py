from django.contrib import admin
from .models import Quiz, Question, MultipleChoice, TextAnswer, Submission

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(MultipleChoice)
admin.site.register(TextAnswer)
admin.site.register(Submission)
