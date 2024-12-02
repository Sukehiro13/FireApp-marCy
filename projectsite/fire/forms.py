from django.forms import ModelForm
from django import forms
from .models import FireStation

class firestationform(ModelForm):
    class Meta: 
        model = FireStation
        fields = "__all__"
        