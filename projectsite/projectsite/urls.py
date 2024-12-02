from django.contrib import admin
from django.urls import path
from fire.views import HomePageView, ChartView, PieCountbySeverity, LineCountbyMonth, MultilineIncidentTop3Country, multipleBarbySeverity, FireStationListView, FireStationCreateView, FireIncidentListView, FireIncidentCreateView, LocationListView, LocationCreateView, LocationUpdateView, LocationDeleteView
from fire import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('dashboard_chart', ChartView.as_view(), name="dashboard-chart"),
    path('chart/', PieCountbySeverity, name="chart"),
    path('lineChart/', LineCountbyMonth, name='chart'),
    path('multilineChart/', MultilineIncidentTop3Country, name='chart'),
    path('multiBarChart/', multipleBarbySeverity, name='chart'),
    path('stations', views.map_station, name='map-station'),
    path('firestations/', FireStationListView.as_view(), name='fire-stations'),
    path('firestations/add/', FireStationCreateView.as_view(), name='fire-stations-add'),
    path('fireincident/', FireIncidentListView.as_view(), name='fire-incidents'),
    path('fireincident/add/', FireIncidentCreateView.as_view(), name='fire-incidents-add'),
    path('location/', LocationListView.as_view(), name='locations'),
    path('location/add/', LocationCreateView.as_view(), name='locations-add'),
    path('location/<pk>/', LocationUpdateView.as_view(), name='locations-edit'),
    path('location/<pk>/delete/', LocationDeleteView.as_view(), name='locations-delete'),
]