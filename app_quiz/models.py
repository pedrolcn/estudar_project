from django.db import models


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
