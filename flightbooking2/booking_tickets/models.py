from django.db import models

class BookingQuota(models.Model):
    """
    Модель для хранения информации о квотах на брониерование
    """
    id_quota = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    max_quota = models.IntegerField(default=5)
    use_quota = models.IntegerField(default=0)

    class Meta:
        db_table = 'booking_quota'


class Booking(models.Model):
    """
    Модель для хранения информации о бронировании
    """
    id_booking = models.BigAutoField(primary_key=True)
    user_name = models.CharField(unique=True, max_length=50)
    dt_booking_created = models.DateTimeField(null=False)
    dt_booking_end = models.DateTimeField(null=False)

    class Meta:
        db_table = 'booking'


class BookingTicket(models.Model):
    """
    Модель для хранения информации о забронированных билетах
    """

    id_ticket = models.BigIntegerField(primary_key=True)
    id_booking = models.BigIntegerField(null=False)
    id_flight = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'booking_tickets'


