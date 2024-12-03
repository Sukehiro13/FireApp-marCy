from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from fire.models import Locations, Incident, FireStation, WeatherConditions, Firefighters, FireTruck

from django.db import connection
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth

from django.db.models import Count
from datetime import datetime
from .forms import firestationform, fireincidentform, locationform, weatherform, firefighterform
from django.urls import reverse_lazy

class HomePageView(ListView):
    model = Locations
    context_object_name = 'home'
    template_name = "home.html"

class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass

def PieCountbySeverity(request):
    query = ''' 
    SELECT severity_level, COUNT(*) as count
    FROM fire_incident
    GROUP BY severity_level
    '''
    data = {}
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    if rows:
        # constructs the dictionary with severity_level as keys and count as values
        data = {severity: count for severity, count in rows}
    else:
        data = {}
    return JsonResponse(data)

def LineCountbyMonth(request):
    current_year = datetime.now().year
    
    result = {month: 0 for month in range(1, 13) }

    incidents_per_month = Incident.objects.filter(date_time__year=current_year) \
        .values_list('date_time', flat=True)

    #counting the number of incidents per month 
    for date_time in incidents_per_month:
        month = date_time.month
        result[month] += 1

    #if you want to convert month numbers to month names, you can use a dictionary mapping
    month_names = {
        1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
        7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec' 
    }

    result_with_month_names = {month_names[int(month)]: count for month, count in result.items()}

    return JsonResponse(result_with_month_names)
 
def MultilineIncidentTop3Country(request): 
 
    query = ''' 
        SELECT  
        fl.country, 
        strftime('%m', fi.date_time) AS month, 
        COUNT(fi.id) AS incident_count 
    FROM  
        fire_incident fi 
    JOIN  
        fire_locations fl ON fi.location_id = fl.id 
    WHERE  
        fl.country IN ( 
            SELECT  
                fl_top.country 
            FROM  
                fire_incident fi_top 
            JOIN  
                fire_locations fl_top ON fi_top.location_id = fl_top.id 
            WHERE  
                strftime('%Y', fi_top.date_time) = strftime('%Y', 'now') 
            GROUP BY  
                fl_top.country 
            ORDER BY  
                COUNT(fi_top.id) DESC 
            LIMIT 3 
        ) 
        AND strftime('%Y', fi.date_time) = strftime('%Y', 'now') 
    GROUP BY  
        fl.country, month 
    ORDER BY  
        fl.country, month; 
    ''' 
 
    with connection.cursor() as cursor: 
        cursor.execute(query) 
        rows = cursor.fetchall() 
 
    # Initialize a dictionary to store the result 
    result = {} 
 
    # Initialize a set of months from January to December 
    months = set(str(i).zfill(2) for i in range(1, 13)) 
 
    # Loop through the query results 
    for row in rows: 
        country = row[0] 
        month = row[1] 
        total_incidents = row[2] 
 
        # If the country is not in the result dictionary, initialize it with all months set to zero 
        if country not in result: 
            result[country] = {month: 0 for month in months} 
 
        # Update the incident count for the corresponding month 
        result[country][month] = total_incidents 
 
    # Ensure there are always 3 countries in the result 
    while len(result) < 3: 
        # Placeholder name for missing countries 
        missing_country = f"Country {len(result) + 1}" 
        result[missing_country] = {month: 0 for month in months} 
 
    for country in result: 
        result[country] = dict(sorted(result[country].items())) 
 
    return JsonResponse(result) 


 
def multipleBarbySeverity(request): 
    query = ''' 
    SELECT  
        fi.severity_level, 
        strftime('%m', fi.date_time) AS month, 
        COUNT(fi.id) AS incident_count 
    FROM  
        fire_incident fi 
    GROUP BY fi.severity_level, month 
    ''' 
 
    with connection.cursor() as cursor: 
        cursor.execute(query) 
        rows = cursor.fetchall() 
 
    result = {} 
    months = set(str(i).zfill(2) for i in range(1, 13)) 
 
    for row in rows: 
        level = str(row[0])  # Ensure the severity level is a string 
        month = row[1] 
        total_incidents = row[2] 
 
        if level not in result: 
            result[level] = {month: 0 for month in months} 
 
        result[level][month] = total_incidents 
 
    # Sort months within each severity level 
    for level in result: 
        result[level] = dict(sorted(result[level].items())) 
 
    return JsonResponse(result) 

def map_station(request):
     fireStations = FireStation.objects.values('name', 'latitude', 'longitude')

     for fs in fireStations:
         fs['latitude'] = float(fs['latitude'])
         fs['longitude'] = float(fs['longitude'])

     fireStations_list = list(fireStations)

     context = {
         'fireStations': fireStations_list,
     }

     return render(request, 'map_station.html', context)
    
class FireStationListView(ListView):
    model = FireStation
    context_object_name = 'stations'
    template_name = 'firestationlist.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fireStations = FireStation.objects.values('name', 'latitude', 'longitude')

        # Convert latitudes and longitudes to float
        for fs in fireStations:
            fs['latitude'] = float(fs['latitude'])
            fs['longitude'] = float(fs['longitude'])

        # Add fireStations to the context
        context['fireStations'] = list(fireStations)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(
                Q(name__icontains=query) | Q(address__icontains=query) | Q(city__icontains=query) | Q(country__icontains=query))
        return qs.order_by('id')

class FireStationCreateView(CreateView):
    model = FireStation
    form_class = firestationform
    template_name = 'firestationadd.html'
    success_url = reverse_lazy('fire-stations')

class FireIncidentListView(ListView):
    model = Incident
    context_object_name = 'incident'
    template_name = 'fire_incident_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(location__icontains=query) | Q(description__icontains=query) | Q(severity_level__icontains=query))
        return queryset.order_by('id')  

class FireStationUpdateView(UpdateView):
    model = FireStation
    form_class = firestationform
    template_name = 'firestationedit.html'
    success_url = reverse_lazy('fire-stations')

class FireStationDeleteView(DeleteView):
    model = FireStation
    template_name = 'firestationdelete.html'
    success_url = reverse_lazy('fire-stations')


class FireIncidentCreateView(CreateView):
    model = Incident
    form_class = fireincidentform
    template_name = 'fire_incident_add.html'
    success_url = reverse_lazy('fire-incidents')

class FireIncidentUpdateView(UpdateView):
    model = Incident
    form_class = fireincidentform
    template_name = 'fire_incident_edit.html'
    success_url = reverse_lazy('fire-incidents')

class FireIncidentDeleteView(DeleteView):
    model = Incident
    template_name = 'fire_incident_delete.html'
    success_url = reverse_lazy('fire-incidents')

class LocationListView(ListView):
    model = Locations
    template_name = 'location_list.html'
    context_object_name = 'locations'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(address__icontains=query) | Q(city__icontains=query) | Q(country__icontains=query))
        return queryset.order_by('id')  

class LocationCreateView(CreateView):
    model = Locations
    form_class = locationform
    template_name = 'location_add.html'
    success_url = reverse_lazy('locations')

class LocationUpdateView(UpdateView):
    model = Locations
    form_class = locationform
    template_name = 'location_edit.html'
    success_url = reverse_lazy('locations')

class LocationDeleteView(DeleteView):
    model = Locations
    template_name = 'location_delete.html'
    success_url = reverse_lazy('locations')

class WeatherConditionListView(ListView):
    model = WeatherConditions
    template_name = 'weather_condition_list.html'
    context_object_name = 'weather'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(incident__description__icontains=query) | Q(temperature__icontains=query) |Q(humidity__icontains=query) |Q(wind_speed__icontains=query) |Q(weather_description__icontains=query))
        return queryset.order_by('id')  

class WeatherConditionCreateView(CreateView):
    model = WeatherConditions
    form_class = weatherform
    template_name = 'weather_condition_add.html'
    success_url = reverse_lazy('weather')

class WeatherConditionUpdateView(UpdateView):
    model = WeatherConditions
    form_class = weatherform
    template_name = 'weather_condition_edit.html'
    success_url = reverse_lazy('weather')

class WeatherConditionDeleteView(DeleteView):
    model = WeatherConditions
    template_name = 'weather_condition_delete.html'
    success_url = reverse_lazy('weather')

class FireFightersListView(ListView):
    model = Firefighters
    template_name = 'firefighterlist.html'
    context_object_name = 'firefighter'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(rank__icontains=query) |Q(experience_level__icontains=query) |Q(station__icontains=query))
        return queryset.order_by('id')  

class FireFightersCreateView(CreateView):
    model = Firefighters
    form_class = firefighterform
    template_name = 'firefighteradd.html'
    success_url = reverse_lazy('fire-fighter')

class FireFightersUpdateView(UpdateView):
    model = Firefighters
    form_class = firefighterform
    template_name = 'firefighteredit.html'
    success_url = reverse_lazy('fire-fighter')

class FireFightersDeleteView(DeleteView):
    model = Firefighters
    template_name = 'firefighterdelete.html'
    success_url = reverse_lazy('fire-fighter')

class FireTruckListView(ListView):
    model = FireTruck
    template_name = 'firetrucklist.html'
    context_object_name = 'firetruck'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(truck_number__icontains=query) | Q(model__icontains=query) |Q(capacity__icontains=query) |Q(station__icontains=query))
        return queryset.order_by('id')


class FireTruckCreateView(CreateView):
    model = Firefighters
    form_class = firefighterform
    template_name = 'firefighteradd.html'
    success_url = reverse_lazy('fire-fighter')