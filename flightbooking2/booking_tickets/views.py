from rest_framework import generics, status
from .models import BookingQuota, Booking, BookingTicket
from .serializers import BookingQuotaSerializer, BookingSerializer, BookingTicketSerializer
from rest_framework.response import Response
import json
from django.http import JsonResponse
import requests
from django.utils import timezone
from datetime import timedelta
from django.db.models import F

# Квоты
class BookingQuotaList(generics.ListCreateAPIView):
    queryset = BookingQuota.objects.all()
    serializer_class = BookingQuotaSerializer

class BookingQuotaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookingQuota.objects.all()
    serializer_class = BookingQuotaSerializer

# Бронирования
class BookingList(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


    def create(self, request, *args, **kwargs):
        # Получение данных из запроса
        body_data_str = str(request.data)  # Преобразовать QueryDict в строку
        body_data = json.loads(body_data_str)  # Парсинг строки в формате JSON

        if body_data is not None:
            tickets = body_data.get('tickets', [])
            flight_number = body_data.get('flight_number')
            # остальной код обработки данных
        else:
            return JsonResponse({'error': 'Invalid request body'})

        # Создание записи в модели Booking
        booking = Booking(user_name=request.user.username, dt_booking_created=timezone.now(), dt_booking_end=timezone.now() + timedelta(days=20))
        booking.save()

        # Создание записей в модели BookingTicket
        booking_tickets = []
        for ticket in tickets:
            booking_ticket = BookingTicket(id_ticket=ticket['ticket_id'], id_booking=booking.id_booking, id_flight=flight_number)
            booking_tickets.append(booking_ticket)

        BookingTicket.objects.bulk_create(booking_tickets)

        # Обновление показателя квоты в объекте BookingQuota
        username = request.user.username
        BookingQuota.objects.filter(username=username).update(use_quota=F('use_quota') + len(booking_tickets))

        serializer = self.get_serializer(booking)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingTicketDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookingTicket.objects.all()
    serializer_class = BookingTicketSerializer

class BookingTicketsByFlight(generics.ListAPIView):
    serializer_class = BookingTicketSerializer

    def get_queryset(self):
        id_flight = self.kwargs['id_flight']
        return BookingTicket.objects.filter(id_flight=id_flight)

class BookingQuotaByUser(generics.ListAPIView):
    serializer_class = BookingQuotaSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    def get_queryset(self):
        username = self.kwargs['username']
        current_datetime = timezone.now()
        queryset = BookingQuota.objects.filter(username=username)
        return queryset

class BookingTicketsByUser(generics.ListAPIView):
    serializer_class = BookingTicketSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response_data = self.get_response_data(queryset)
        serialized_data = json.dumps(response_data)
        return JsonResponse(response_data, safe=False)

    def get_queryset(self):
        username = self.kwargs['username']
        current_datetime = timezone.now()

        # Шаг 1: Получить все атрибуты id_booking из модели Booking, где дата окончания брони еще не наступила
        bookings = Booking.objects.filter(user_name=username, dt_booking_end__gt=current_datetime)

        # Шаг 2: Забрать все записи из модели BookingTicket
        queryset = BookingTicket.objects.filter(id_booking__in=bookings)
        return queryset


    def get_response_data(self, queryset):
        # Шаги 3-5: Формирование response_data

        id_flights = queryset.values_list('id_flight', flat=True).distinct()
        print('Отправляем запрос на сервис airs, чтобы получить данные рейсов')
        flights_data = []
        for id_flight in id_flights:
            url = f'http://127.0.0.1:8000/api/flights/{id_flight}/?format=json'
            response = requests.get(url, headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                flight_data = response.json()
                flights_data.append(flight_data)

        response_data = []
        for booking_ticket in queryset:
            flight_data = next((flight for flight in flights_data if flight['id_flight'] == booking_ticket.id_flight), None)
            if flight_data:
                response_entry = {
                    'id_flight': flight_data['id_flight'],
                    'id_ticket': booking_ticket.id_ticket,
                    'departure_date': flight_data['departure_time'],
                    'arrival_date': flight_data['arrival_time']
                }
                response_data.append(response_entry)

        return response_data

# Забронированные билеты
class BookingTicketList(generics.ListCreateAPIView):
    serializer_class = BookingTicketSerializer

    def get_queryset(self):
        queryset = BookingTicket.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        data = json.loads(request.data)
        ticket_ids = data.get('tickets', [])
        id_list = [item['ticket_id'] for item in ticket_ids]
        queryset = self.get_queryset().filter(id_ticket__in=id_list)
        queryset.delete()

        # Обновление показателя квоты в объекте BookingQuota
        username = request.user.username
        BookingQuota.objects.filter(username=username).update(use_quota=F('use_quota') - len(id_list))

        return Response({}, status=status.HTTP_204_NO_CONTENT)

