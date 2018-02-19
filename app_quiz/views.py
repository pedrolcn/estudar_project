from uuid import uuid4
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.utils import timezone
from django.db.models import Count, Sum
from django.urls import reverse

from .models import Quiz, Question, MultipleChoice, TextAnswer, Submission


class IndexView(generic.ListView):
    template_name = 'app_quiz/index.html'
    context_object_name = 'latest_quiz_list'

    def get_queryset(self):
        """ Return the last 5 published questions"""
        return Quiz.objects.filter(
            pub_date__lte=timezone.now()).order_by('pub_date')


class QuizView(generic.DetailView):
    model = Quiz
    template_name = 'app_quiz/quiz.html'


def results(request, quiz_id):

    correct_answers = 0
    points = 0

    submission = Submission.objects.filter(
        quiz__id__exact=quiz_id).order_by('-pub_date')[0]

    if not submission:
        # Catch empty queryset
        raise Http404(
            "There is no quiz associated with the given id=%d" % quiz_id)

    quiz = get_object_or_404(Quiz.objects.annotate(
        num_questions=Count('question'),
        max_points=Sum('question__value')), pk=quiz_id)

    answer_set = submission.get_answers()
    answer_display = []

    for i, question in enumerate(quiz.question_set.all()):
        display_dict = {}
        display_dict['question'] = question
        display_dict['isCorrect'] = False
        display_dict['correct_answer'] = question.get_correct_answer()
        if not question.textAnswer:
                choice = MultipleChoice.objects.get(pk=answer_set[i])
                display_dict['answer'] = choice.text

                if choice.isCorrectAnswer:
                    correct_answers += 1
                    points += question.value
                    display_dict['isCorrect'] = True

        else:
            text_answer = get_object_or_404(TextAnswer, question=question)
            display_dict['answer'] = text_answer

            if answer_set[i] == text_answer.correctAnswer:
                correct_answers += 1
                points += question.value
                display_dict['isCorrect'] = True

        answer_display.append(display_dict)

    context_dict = {
        'quiz': quiz,
        'answers': answer_display,
        'correct_answers': correct_answers,
        'points': points
    }

    return render(request, 'app_quiz/results.html', context_dict)


def submit(request, quiz_id):

    answer_set = []
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    # Setup responses in case cookie needs to be set
    redirect = HttpResponseRedirect(reverse('app_quiz:results',
                                    args=(quiz_id,)))
    error_response = render(request, 'app_quiz/quiz.html', {
        'quiz': Quiz.objects.get(pk=quiz_id),
        'error_message': "You didn't answer all questions."
    })

    # Setting a hash in the cookies and in the submissions table altough it
    # provides limited user_id functionality, here is done to prevent race
    # conditions when two users are submitting to the same questions, it then
    # provides means to differentiate between their answers as each user will
    # have a unique hash_id for the duration of their browser session
    hash_id = request.COOKIES.get('hash_id')
    if not hash_id:
        hash_id = uuid4()
        redirect.set_cookie('hash_id', hash_id)
        error_response.set_cookie('hash_id', hash_id)

    submission = Submission(quiz=quiz, hash_id=hash_id)

    for question in quiz.question_set.all():
        try:
            answer = request.POST['question%d' % question.id]
            if not answer:
                # Catch empty strings in text answers
                raise KeyError(question.id)

        except KeyError:
            return error_response

        else:
            answer_set.append(answer)

    submission.set_answers(answer_set)
    submission.save()

    return redirect
