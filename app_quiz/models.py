from django.db import models
import json


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    value = models.IntegerField(default=1)
    # Assumes that if answer is not text it is multiple choice
    textAnswer = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def get_correct_answer(self):
        if self.textAnswer:
            return TextAnswer.objects.get(question=self.id).correctAnswer

        else:
            # Exploits the fact that there SHOULD be only one correct option
            for item in self.multiplechoice_set.all():
                if item.isCorrectAnswer:
                    return item.text


class MultipleChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    isCorrectAnswer = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class TextAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correctAnswer = models.CharField(max_length=255)

    def __str__(self):
        return self.correctAnswer


class Submission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answers = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    hash_id = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.quiz.name + " answers"

    # List field from json evil hack
    def set_answers(self, x):
        self.answers = json.dumps(x)

    def get_answers(self):
        # I WANT ANSWERS
        return json.loads(self.answers)
