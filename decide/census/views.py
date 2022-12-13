from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
import csv
from base.perms import UserIsStaff
from .models import Census
from voting.models import Voting
from django.core import serializers

def first_view(request):
    census_list = Census.objects.all()
    voting_list=Voting.objects.all()
    user_list=User.objects.all()
    t=len(voting_list)
    t1=len(user_list)
    user=User.objects.get(id=1).username
    voting=Voting.objects.get(id=2).name
    context = {'object_list': census_list,'u': user,'b': voting,'t': t,'t1': t1}
    return render(request, 'census/census.html', context)
def exportcsv(request):
    #print('entro')
    students = Census.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=censo.csv'
    writer = csv.writer(response)
    writer.writerow(['VotingID', 'VoterID'])
    
    #print(user)
    #print(voting)
    
    #studs = students.values_list('voting_id','voter_id')
    for std in students:
       user=User.objects.get(id=std.voter_id).username
       voting=Voting.objects.get(id=std.voting_id).name
       writer.writerow([voting, user])
    return response    
def exportjson(request):
    all_census = Census.objects.all()
    cenus_list = serializers.serialize('json', all_census)
    return HttpResponse(cenus_list, content_type="text/json-comment-filtered")
def exportxml(request):
    all_census = Census.objects.all()
    cenus_list = serializers.serialize('xml', all_census)
    return HttpResponse(cenus_list, content_type="text/xml")

class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        type = request.data.get('type')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter,type=type)
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})


class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        type= request.data.get('type')
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters, type=type)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')
