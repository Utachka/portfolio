from rest_framework import generics, response
from .models import Flight, Ticket, Aircraft, Country
from .serializers import FlightSerializer, CountrySerializer, AircraftSerializer, TicketSerializer

class FlightList(generics.ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def list(self, request, *args, **kwargs):
        flights = self.get_queryset()
        serializer = self.get_serializer(flights, many=True)

        # Заменяем идентификаторы стран на их наименования
        for data in serializer.data:
            country_source_id = data['country_source_id']
            country_target_id = data['country_target_id']

            country_source = Country.objects.get(id_country=country_source_id)
            country_target = Country.objects.get(id_country=country_target_id)

            data['country_source'] = country_source.name
            data['country_target'] = country_target.name

            del data['country_source_id']
            del data['country_target_id']
        return response.Response(serializer.data)

class FlightDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class CountryList(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class TicketList(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketListByFlight(generics.ListAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        flight_id = self.kwargs['flight_id']
        return Ticket.objects.filter(id_flight=flight_id)


class AircraftList(generics.ListCreateAPIView):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

class AircraftDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer