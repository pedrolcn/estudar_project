from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.db.models import Count, Sum

from .models import Quiz, Question, MultipleChoice, TextAnswer


class IndexView(generic.ListView):
    template_name = 'app_quiz/index.html'
    context_object_name = 'latest_quiz_list'

    def get_queryset(self):
        """ Return the last 5 published questions"""
        return Quiz.objects.filter(
            pub_date__lte=timezone.now()).order_by('pub_date')


class DetailView(generic.DetailView):
    model = Quiz
    template_name = 'app_quiz/quiz.html'


class ResultsView(generic.DetailView):
    model = Quiz
    template_name = 'app_quiz/results.html'


def submit(request, quiz_id):

    right_answers = 0
    points = 0
    answers = []

    quiz = get_object_or_404(Quiz.objects.annotate(
        num_questions=Count('question'),
        max_points=Sum('question__value')), pk=quiz_id)

    q_num = quiz.num_questions
    max_pt = quiz.max_points

    for question in quiz.question_set.all():
        try:
            answer = request.POST['question%d' % question.id]
            if not answer:
                # Catch empty strings in text answers
                raise KeyError(question.id)
        except KeyError:
            return render(request, 'app_quiz/quiz.html',
                          {
                              'quiz': Quiz.objects.get(pk=quiz_id),
                              'error_message': "You didn't answer all questions."
                          })
        else:
            if not question.textAnswer:
                choice = MultipleChoice.objects.get(pk=answer)

                if choice.isCorrectAnswer:
                    right_answers += 1
                    points += question.value
            else:
                text_answer = question.textanswer_set.all()[0]

                if answer == text_answer.correctAnswer:
                    right_answers += 1
                    points += question.value

            answers.append(answer)

    context_dict = {
        'quiz': quiz,
        'right_answers': right_answers,
        'max_pt': max_pt,
        'q_num': q_num,
        'answers': answers,
        'points': points
    }

    return render(request, 'app_quiz/submit.html', context_dict)
