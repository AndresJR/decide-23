from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.indexCensus, name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('reuseCensusV2/V/', views.reuseCensusV2),
    path('reuseCensusV2/BV/', views.reuseCensusV2BV),
    path('censusForAll/V/', views.censusForAll),
    path('censusForAll/BV/', views.censusForAllBV),
    path('prueba', views.prueba),



    
]
