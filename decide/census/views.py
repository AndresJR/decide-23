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
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
import csv
import xml
from base.perms import UserIsStaff
from .models import Census
from voting.models import Voting
from django.core import serializers
from .forms import NameForm


def first_view(request):
    census_list = Census.objects.all()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            id= form.cleaned_data['q']
            v= form.cleaned_data['x']
            if id:
                census_list = Census.objects.all()
                #voter=get_object_or_404(User,id=id)
                like=User.objects.filter(username__contains=id)
                for u in like:
                    census_list = census_list.filter(voter_id=u.id)
            else:
                census_list = Census.objects.all()
            if v:
                
                #voter=get_object_or_404(User,id=id)
                like=Voting.objects.filter(name__contains=v)
                for vo in like:
                    census_list = census_list.filter(voting_id=vo.id)
            
        
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
        
        census_list = Census.objects.all()
    voting_list=Voting.objects.all()
    user_list=User.objects.all()
    t=len(voting_list)
    t1=len(user_list)
    user=User.objects.get(id=1).username
    voting=Voting.objects.get(id=2).name
    context = {'object_list': census_list,'u': user,'b': voting,'t': t,'t1': t1,'form':form}
    return render(request, 'census/census.html',context)
def exportcsv(request):
    #print('entro')
    lista_census = Census.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=censo.csv'
    writer = csv.writer(response)
    writer.writerow(['VotingID', 'VoterID','Tipo'])
    
    #print(user)
    #print(voting)
    
    #censos = lista_census.values_list('voting_id','voter_id')
    for c in lista_census:
       user=User.objects.get(id=c.voter_id).username
       voting=Voting.objects.get(id=c.voting_id).name
       writer.writerow([voting, user,c.type])
    return response    
def exportjson(request):
    all_census = Census.objects.all()
    cenus_list = serializers.serialize('json', all_census)
    response = HttpResponse(cenus_list, content_type="text/json-comment-filtered")
    response['Content-Disposition'] = 'attachment; filename=censo.json'
    
    return response
def exportxml(request):
    all_census = Census.objects.all()
    cenus_list = serializers.serialize('xml', all_census)
    response=HttpResponse(cenus_list, content_type="text/xml")
    response['Content-Disposition'] = 'attachment; filename=censo.xml'
    return response




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
