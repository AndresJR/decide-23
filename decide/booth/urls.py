from django.urls import path
from .views import BoothView, ScoreBoothView


urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('scoreVoting/<int:voting_id>/', ScoreBoothView.as_view()),
]
