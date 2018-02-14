from django.urls import path
from . import views

app_name = "app_quiz"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.QuizView.as_view(), name='quiz'),
    path('<int:submission_id>/results/', views.results, name='results'),
    path('<int:quiz_id>/submit/', views.submit, name='submit')
]
