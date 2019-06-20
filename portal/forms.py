from django import forms
from .models import MapNote

class MapNoteForm(forms.ModelForm):
    name = forms.CharField()
    note = forms.CharField(widget=forms.Textarea)


    class Meta:
        model = MapNote
        fields = ['name','note']
