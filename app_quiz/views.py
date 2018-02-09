from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils import timezone

from .models import Quiz


class IndexView(generic.ListView):
    template_name = 'app_quiz/index.html'
    context_object_name = 'latest_quiz_list'

    def get_queryset(self):
        """ Return the last 5 published questions"""
        return Quiz.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Quiz
    template_name = 'app_quiz/details.html'


class ResultsView(generic.DetailView):
    model = Quiz
    template_name = 'app_quiz/results.html'


def submit(request, quiz_id):
    return HttpResponse("you are submiting your answers to quiz %i" % quiz_id)
