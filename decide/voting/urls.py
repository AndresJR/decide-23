from django.urls import path
from . import views


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('votingbinary/', views.VotingBinaryView.as_view(), name = 'votingbinary'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
]
