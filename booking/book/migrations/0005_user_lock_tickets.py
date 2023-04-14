# Generated by Django 4.1.2 on 2023-04-13 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_booking_quota'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_lock_tickets',
            fields=[
                ('username', models.CharField(max_length=150)),
                ('id_flight', models.BigIntegerField()),
                ('id_ticket', models.BigIntegerField(primary_key=True, serialize=False)),
                ('seat_number', models.IntegerField()),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('country_source', models.CharField(max_length=50)),
                ('country_target', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'v_user_lock_tickets',
                'managed': False,
            },
        ),
    ]
