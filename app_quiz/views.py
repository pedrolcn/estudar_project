from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.db.models import Count

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
    answers = []

    quiz = Quiz.objects.annotate(num_questions=Count('question')).get(pk=quiz_id)
    q_num = quiz.num_questions

    for question in quiz.question_set.all():
        try:
            answer = request.POST['question%d' % question.id]
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
            else:
                text_answer = question.textanswer_set.all()[0]

                if answer == text_answer.correctAnswer:
                    right_answers += 1

            answers.append(answer)

    context_dict = {
        'quiz': quiz,
        'right_answers': right_answers,
        'q_num': q_num,
        'answers': answers
    }

    return render(request, 'app_quiz/submit.html', context_dict)
