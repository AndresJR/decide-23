from django.urls import path
from . import views


urlpatterns = [
   

    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),

    path('binaryVoting/', views.VotingBinaryView.as_view(), name='binaryVoting'),
    path('binaryVoting/<int:voting_id>/', views.VotingBinaryUpdate.as_view(), name='binaryVoting'),
    
    path('scoreVoting/', views.ScoreVotingView.as_view(), name='scoreVoting'),
    path('scoreVoting/<int:voting_id>/', views.ScoreVotingUpdate.as_view(), name='scoreVoting')

]
