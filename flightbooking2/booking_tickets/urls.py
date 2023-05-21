from rest_framework.urlpatterns import format_suffix_patterns
from .views import BookingQuotaDetail, BookingQuotaList, BookingList, BookingDetail, BookingTicketList, BookingTicketDetail, BookingTicketsByFlight, BookingTicketsByUser, BookingQuotaByUser
from django.urls import path, include


urlpatterns = format_suffix_patterns([
    path('api/bookingQuotas/', BookingQuotaList.as_view(), name='bookingQuota'),
    path('api/bookingQuotas/<int:pk>/', BookingQuotaDetail.as_view(), name='bookingQuota-detail'),
    path('api/bookingQuotasByUser/<str:username>/', BookingQuotaByUser.as_view(), name='bookingQuotaByUser'),

    path('api/bookings/', BookingList.as_view(), name='booking'),
    path('api/bookings/<int:pk>/', BookingDetail.as_view(), name='booking-detail'),


    path('api/bookingTickets/<int:pk>/', BookingTicketDetail.as_view(), name='bookingTicket-detail'),
    path('api/flights/<int:id_flight>/bookingTickets/', BookingTicketsByFlight.as_view(), name='booking-Tickets-By-Flight'),
    path('api/bookingTickets/', BookingTicketList.as_view(), name='bookingTicket'),
    path('api/user/<str:username>/bookingTickets/', BookingTicketsByUser.as_view(), name='booking-Tickets-By-User'),

])