from rest_framework import serializers
from .models import BookingQuota, Booking, BookingTicket

class BookingQuotaSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели BookingQuota
    """
    class Meta:
        model = BookingQuota
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Booking
    """
    class Meta:
        model = Booking
        fields = '__all__'


class BookingTicketSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели BookingTickets
    """
    class Meta:
        model = BookingTicket
        fields = '__all__'