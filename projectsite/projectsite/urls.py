from django.contrib import admin
from django.urls import path
from fire.views import HomePageView, FireTruckListView, FireTruckDeleteView, FireTruckUpdateView, FireTruckCreateView, FireStationDeleteView, FireFightersCreateView, FireFightersDeleteView, FireFightersUpdateView, FireFightersListView, ChartView, FireStationUpdateView, PieCountbySeverity, LineCountbyMonth, MultilineIncidentTop3Country, multipleBarbySeverity, FireStationListView, FireStationCreateView, FireIncidentListView, FireIncidentCreateView, LocationListView, LocationCreateView, LocationUpdateView, LocationDeleteView, FireIncidentUpdateView, FireIncidentDeleteView, WeatherConditionListView, WeatherConditionCreateView, WeatherConditionUpdateView, WeatherConditionDeleteView
from fire import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', ChartView.as_view(), name="dashboard-chart"),
    path('chart/', PieCountbySeverity, name="chart"),
    path('lineChart/', LineCountbyMonth, name='chart'),
    path('multilineChart/', MultilineIncidentTop3Country, name='chart'),
    path('multiBarChart/', multipleBarbySeverity, name='chart'),
    path('stations', views.map_station, name='map-station'),
    path('firestations/', FireStationListView.as_view(), name='fire-stations'),
    path('firestations/add/', FireStationCreateView.as_view(), name='fire-stations-add'),
    path('firestations/<pk>/', FireStationUpdateView.as_view(), name='fire-stations-edit'),
    path('firestations/<pk>/delete/', FireStationDeleteView.as_view(), name='fire-stations-delete'),
    path('fireincident/', FireIncidentListView.as_view(), name='fire-incidents'),
    path('fireincident/add/', FireIncidentCreateView.as_view(), name='fire-incidents-add'),
    path('fireincident/<pk>/', FireIncidentUpdateView.as_view(), name='fire-incidents-edit'),
    path('fireincident/<pk>/delete/', FireIncidentDeleteView.as_view(), name='fire-incidents-delete'),
    path('location/', LocationListView.as_view(), name='locations'),
    path('location/add/', LocationCreateView.as_view(), name='locations-add'),
    path('location/<pk>/', LocationUpdateView.as_view(), name='locations-edit'),
    path('location/<pk>/delete/', LocationDeleteView.as_view(), name='locations-delete'),
    path('weathercondition/', WeatherConditionListView.as_view(), name='weather'),
    path('weathercondition/add/', WeatherConditionCreateView.as_view(), name='weather-add'),
    path('weathercondition/<pk>/', WeatherConditionUpdateView.as_view(), name='weather-edit'),
    path('weathercondition/<pk>/delete/', WeatherConditionDeleteView.as_view(), name='weather-delete'),
    path('firefighters/', FireFightersListView.as_view(), name='fire-fighter'),
    path('firefighters/add/', FireFightersCreateView.as_view(), name='fire-fighter-add'),
    path('firefighter/<pk>/', FireFightersUpdateView.as_view(), name='fire-fighter-edit'),
    path('firefighter/<pk>/delete/', FireFightersDeleteView.as_view(), name='fire-fighter-delete'),
    path('firetrucks/', FireTruckListView.as_view(), name='fire-truck'),
    path('firetruck/add/', FireTruckCreateView.as_view(), name='fire-truck-add'),
    path('firetruck/<pk>/', FireTruckUpdateView.as_view(), name='fire-truck-edit'),
    path('firetruck/<pk>/delete/', FireTruckDeleteView.as_view(), name='fire-truck-delete'),
]