from django.urls import path
from gateway.views import gateway_view, gateway_view_tickets_by_flight, gateway_view_booking_tickets_user, gateway_view_quota

urlpatterns = [
    # сервис перелетов
    path('flights/', gateway_view, name='gateway-flights'),
    path('flights/<int:pk>/', gateway_view, name='gateway-flight'),
    path('tickets/', gateway_view, name='gateway-tickets'),

    # сервис бронирования
    path('bookings/', gateway_view, name='gateway-bookings'),
    path('bookings/<int:pk>/', gateway_view, name='gateway-booking'),
    path('bookingQuotas/', gateway_view, name='bookingQuotas-bookings'),
    path('bookingQuotas/<int:pk>/', gateway_view, name='bookingQuotas-booking'),
    path('bookingTickets/', gateway_view, name='bookingTickets-bookings'),
    path('bookingTickets/<int:pk>/', gateway_view, name='bookingTickets-booking'),
    path('flights/<int:pk>/tickets/', gateway_view_tickets_by_flight, name='ticket-list-by-flight'),
    path('gateway/<str:username>/bookingTickets/', gateway_view_booking_tickets_user, name='gateway_view_booking_tickets_user'),
    path('gateway/bookingQuotasByUser/<str:username>/', gateway_view_quota, name='gateway_view_quota')
]
