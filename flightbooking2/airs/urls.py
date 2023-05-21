from rest_framework.urlpatterns import format_suffix_patterns
from .views import FlightList, FlightDetail, TicketListByFlight, CountryList, CountryDetail, TicketList, TicketDetail, AircraftDetail, AircraftList
from django.urls import path, include


urlpatterns = format_suffix_patterns([
    path('api/flights/', FlightList.as_view(), name='flight-list'),
    path('api/flights/<int:pk>/', FlightDetail.as_view(), name='flight-detail'),
    path('api/flights/<int:flight_id>/tickets/', TicketListByFlight.as_view(), name='ticket-list-by-flight'),

    path('api/countrys/', CountryList.as_view(), name='country-list'),
    path('api/countrys/<int:pk>/', CountryDetail.as_view(), name='country-detail'),

    path('api/tickets/', TicketList.as_view(), name='ticket-list'),
    path('api/tickets/<int:pk>/', TicketDetail.as_view(), name='ticket-detail'),

    path('api/aircrefts/', AircraftList.as_view(), name='aircraft-list'),
    path('api/aircrafts/<int:pk>/', AircraftDetail.as_view(), name='aircraft-detail'),
])

