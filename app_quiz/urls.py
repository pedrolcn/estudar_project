from django.urls import path
from . import views

app_name = "app_quiz"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='quiz'),
    path('<int:pk>/result/', views.ResultsView.as_view(), name='results'),
    path('<int:quiz_id>/submit/', views.submit, name='submit')
]
