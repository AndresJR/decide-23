
from voting.models import ScoreVoting

from django.shortcuts import get_object_or_404

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from census.models import Census
from voting.models import Voting, VotingBinary
import django_filters.rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import Vote
from .serializers import VoteSerializer
from base import mods
from base.perms import UserIsStaff


class StoreView(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('voting_id', 'voter_id')

    def get(self, request):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        return super().get(request)

    def post(self, request):
        """
         * voting: id
         * voter: id
         * vote: { "a": int, "b": int }
        """

        
        vid = request.data.get('voting')
        uid = request.data.get('voter')
        vote = request.data.get('vote')
        type = request.data.get('type')
        print(vid)
        


        if(Voting.objects.filter(id=vid).exists()):
            type='V'
        elif(VotingBinary.objects.filter(id=vid).exists()):
            type='BV'
        else:
            type='SV'
        print(type)
        print(vote)

        if type=='BV':
            voting = get_object_or_404(VotingBinary,pk=vid)
            print(voting)        
        else:
            voting = get_object_or_404(Voting,pk=vid)
            print(voting)

        if not vid or not uid or not vote:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        if not vid or not uid or not vote:
            print('e1')
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        start_date = voting.start_date
        end_date = voting.end_date
        not_started = not start_date or timezone.now() < start_date
        is_closed = end_date and end_date < timezone.now()
        
        
        if not_started or is_closed:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)


        # validating voter
        token = request.auth.key
        #print(token)
        voter = mods.post('authentication', entry_point='/getuser/', json={'token': token})
        #print(voter)
        voter_id = voter.get('id', None)
        if not voter_id or voter_id != uid:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        # the user is in the census

        if type == 'SV':
            try:
                perms = Census.objects.get(voting_id=vid,voter_id=voter_id,type='SV')
                print(perms)
            except:
                return Response({}, status=status.HTTP_401_UNAUTHORIZED) 

        elif type == 'BV':
            try:
                perms = Census.objects.get(voting_id=vid,voter_id=voter_id,type='BV')

                print(perms)
            except:
                return Response({}, status=status.HTTP_401_UNAUTHORIZED) 
        else:
            try:
                perms = Census.objects.get(voting_id=vid,voter_id=voter_id,type='V')
                print(perms)
            except:
                return Response({}, status=status.HTTP_401_UNAUTHORIZED)

     #Comprobamos que el voto está registrado
        voto_registrado = Vote.objects.filter(voting_id=vid, voter_id=uid, type=voting.type)
            
        if voto_registrado:
                #En caso de editar el voto
                #Se elimina  el voto anterior registrado
            for vt in voto_registrado:
                    vt.delete()

            a = vote.get("a")
            b = vote.get("b")

            defs = { "a": a, "b": b }
            v, _ = Vote.objects.get_or_create(voting_id=vid, voter_id=uid, defaults=defs, type=voting.type)
            v.a = a
            v.b = b


        else:
            a = vote.get("a")
            b = vote.get("b")

            defs = { "a": a, "b": b }
            v, _ = Vote.objects.get_or_create(voting_id=vid, voter_id=uid, defaults=defs, type=voting.type)
            v.a = a
            v.b = b


            defs = { "a": a, "b": b }
            v, _ = Vote.objects.get_or_create(voting_id=vid, voter_id=uid,
                                            defaults=defs, type=voting.type)
            v.a = a
            v.b = b

        v.save()
        
        return  Response({})
