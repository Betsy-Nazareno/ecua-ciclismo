# Generated by Django 3.2.6 on 2022-08-13 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruta', '0010_auto_20220811_0121'),
    ]

    operations = [
        migrations.AddField(
            model_name='ruta',
            name='finalizado',
            field=models.BooleanField(default=0),
        ),
    ]