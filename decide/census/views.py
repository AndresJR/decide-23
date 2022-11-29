from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)

from base.perms import UserIsStaff
from .models import Census
from django.contrib.auth.models import User

class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter)
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})


def reuseCensus(request, oldVotingId, newVotingId):
    census = Census.objects.filter(voting_id=oldVotingId)
    try:
        for censo in census:
            censo_repe = Census.objects.filter(voting_id=newVotingId,voter_id=censo.voter_id)
            if len(censo_repe) == 0:
                voter = censo.voter_id
                reuseCenso = Census(voting_id=newVotingId, voter_id=voter)
                reuseCenso.save()
    except IntegrityError:
            return HttpResponse('no se ha podido crear el censo')
    return HttpResponse('se ha creado el censo correctamente')

def censusForAll(request, voting_id):
    voters = User.objects.all()
    id_repetidas = ""
    
    for voter in voters:
        id = voter.id
        censo_repe=Census.objects.filter(voting_id=voting_id,voter_id=id)
        if len(censo_repe) == 0:     
            census = Census(voting_id=voting_id, voter_id=id)
            census.save()
        else: 
            id_repetidas += (str(id)+",")
    print(id_repetidas)    
    return render(request, './reuseCensus.html',{'id_repeti':id_repetidas})
    
    
    
    



class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')
