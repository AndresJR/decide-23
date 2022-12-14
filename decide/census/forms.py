from django import forms

class NameForm(forms.Form):
    q = forms.CharField(required=False,label='Votante', max_length=100)
    x = forms.CharField(required=False,label='Votación', max_length=100)

    