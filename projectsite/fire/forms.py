from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import now, make_aware
from .models import FireStation, Incident, Locations, WeatherConditions, Firefighters, FireTruck

class firestationform(ModelForm):
    class Meta: 
        model = FireStation
        fields = "__all__"

class fireincidentform(ModelForm):
    class Meta: 
        model = Incident
        fields = ['location', 'date_time', 'severity_level', 'description']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',  # HTML5 input for datetime picker
                'class': 'form-control',  # Optional: Bootstrap styling
            }),
        }

    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')

        # Convert to timezone-aware if it's naive
        if date_time is not None and date_time.tzinfo is None:
            date_time = make_aware(date_time)

        # Compare with the current time
        if date_time > now():
            raise ValidationError("The date and time cannot be in the future.")
        return date_time
        
class locationform(ModelForm):
    class Meta: 
        model = Locations
        fields = "__all__"

class weatherform(ModelForm):
    class Meta: 
        model = WeatherConditions
        fields = "__all__"
        widgets = {
            'temperature': forms.NumberInput(attrs={'min': '0', 'step': '0.01', 'class': 'form-control'}),
            'humidity': forms.NumberInput(attrs={'min': '0', 'step': '0.01', 'class': 'form-control'}),
            'wind_speed': forms.NumberInput(attrs={'min': '0', 'step': '0.01', 'class': 'form-control'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fields_to_validate = ['temperature', 'humidity', 'wind_speed']

        for field in fields_to_validate:
            value = cleaned_data.get(field)
            if value is not None and value < 0:
                self.add_error(field, f"{field.replace('_', ' ').capitalize()} must be non-negative.")
        return cleaned_data

class firefighterform(ModelForm):
    class Meta: 
        model = Firefighters
        fields = "__all__"

class firetruckform(ModelForm):
    class Meta: 
        model = FireTruck
        fields = "__all__"