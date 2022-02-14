# Generated by Django 4.0.2 on 2022-02-13 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('time', models.CharField(max_length=50)),
                ('temperature', models.FloatField()),
                ('wind_direction', models.CharField(max_length=50)),
                ('wind_speed', models.FloatField()),
                ('weather_kod', models.CharField(max_length=20)),
                ('cloud_number', models.IntegerField()),
            ],
        ),
    ]