from django.forms import ModelForm
from django import forms
from .models import FireStation, Incident, Locations

class firestationform(ModelForm):
    class Meta: 
        model = FireStation
        fields = "__all__"

class fireincidentform(ModelForm):
    class Meta: 
        model = Incident
        fields = "__all__"
        
class locationform(ModelForm):
    class Meta: 
        model = Locations
        fields = "__all__"