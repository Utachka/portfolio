# Generated by Django 4.1.2 on 2023-05-15 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id_flight', models.BigAutoField(primary_key=True, serialize=False)),
                ('country_source_id', models.BigIntegerField()),
                ('country_target_id', models.BigIntegerField()),
                ('id_air', models.BigIntegerField()),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'flights',
                'managed': False,
            },
        ),
    ]
