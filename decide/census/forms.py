'''from django import forms
from .models import Census


census = Census.objects.all()
set_censos=set();
for censo in census:
    set_censos.add(censo.voting_id)




class CreateReuseCensus(forms.Form):
    OldVotingId = forms.ChoiceField(choices=set_censos)
    NewVotingId = forms.ChoiceField(choices=set_censos)'''
