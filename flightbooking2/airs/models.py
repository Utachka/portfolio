
from django.db import models

class Country(models.Model):

    id_country = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)

    class Meta:
        managed = False # указываем, что Django не должен управлять таблицей
        db_table = 'countrys'

class Flight(models.Model):
    """
    Модель для хранения информации о рейсах
    """
    id_flight = models.BigAutoField(primary_key=True)
    country_source_id = models.BigIntegerField()
    country_target_id = models.BigIntegerField()
    id_air = models.BigIntegerField()
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        managed = False # указываем, что Django не должен управлять таблицей
        db_table = 'flights'

    def country_source_name(self):
        country = Country.objects.get(id=self.country_source_id)
        return country.name

    def country_target_name(self):
        country = Country.objects.get(id=self.country_target_id)
        return country.name


class Aircraft(models.Model):

    id_air = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    count_sits = models.IntegerField(null=False)

    class Meta:
        managed = False # указываем, что Django не должен управлять таблицей
        db_table = 'aircrafts'


class Ticket(models.Model):

    id_ticket = models.BigAutoField(primary_key=True)
    id_flight = models.BigIntegerField(null=False)
    seat_number = models.IntegerField(null=False)

    class Meta:
        managed = False # указываем, что Django не должен управлять таблицей
        db_table = 'tickets'