from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('reuseCensusV2/', views.reuseCensusV2),
    #path('reuseCensus/<int:oldVotingId>/<int:newVotingId>', views.reuseCensus),
    path('censusForAll/<int:voting_id>', views.censusForAll),
    path('prueba', views.prueba),



    
]
