from rest_framework import serializers
from .models import Flight, Aircraft, Ticket, Country

class FlightSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Flight
    """
    class Meta:
        model = Flight
        fields = '__all__'


class AircraftSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Flight
    """
    class Meta:
        model = Aircraft
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Flight
    """
    class Meta:
        model = Country
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Flight
    """
    class Meta:
        model = Ticket
        fields = '__all__'