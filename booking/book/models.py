from django.db import models

class Aircraft(models.Model):
    id_air = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    count_sits = models.IntegerField()

    class Meta:
        managed = False # указываем, что Django не должен управлять таблицей
        db_table = 'aircraft'
        verbose_name = 'Самолет'
        verbose_name_plural = 'Самолеты'

class Flight_list(models.Model):
    number_flight = models.BigIntegerField(primary_key=True)
    country_source = models.CharField(max_length=50)
    country_target = models.CharField(max_length=50)
    air_name = models.CharField(max_length=50)
    count_sits = models.IntegerField()
    count_free_tickets = models.IntegerField()
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        managed = False # указываем, что Django не должен управлять таблицей
        db_table = 'v_flight_list'


class Flight_detail(models.Model):
    id_ticket = models.BigIntegerField(primary_key=True)
    id_flight = models.BigIntegerField(null=False)
    seat_number = models.IntegerField(null=False)
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'tickets'


class Booking_quota(models.Model):
    username = models.CharField(primary_key=True, max_length=150)
    all_quota = models.IntegerField(null=False)
    use_quota = models.IntegerField(null=False)

    class Meta:
        managed = False
        db_table = 'booking_quota'

class User_lock_tickets(models.Model):
    username = models.CharField(max_length=150, null=False)
    id_flight = models.BigIntegerField(null=False)
    id_ticket = models.BigIntegerField(primary_key=True, null=False)
    seat_number = models.IntegerField(null=False)
    departure_time = models.DateTimeField(null=False)
    arrival_time = models.DateTimeField(null=False)
    country_source = models.CharField(max_length=50, null=False)
    country_target = models.CharField(max_length=50, null=False)

    class Meta:
        managed = False
        db_table = 'v_user_lock_tickets'