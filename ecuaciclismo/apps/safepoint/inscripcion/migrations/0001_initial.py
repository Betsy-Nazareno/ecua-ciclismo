# Generated by Django 3.2.6 on 2024-12-31 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReservaRuta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentarios', models.TextField(blank=True, null=True)),
                ('horas', models.FloatField(blank=True, null=True)),
                ('kilocalorias', models.FloatField(blank=True, null=True)),
                ('kilometros', models.FloatField(blank=True, null=True)),
                ('velocidad', models.FloatField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')),
                ('ultimo_cambio', models.DateTimeField(auto_now=True, db_column='ultimo_cambio')),
            ],
            options={
                'db_table': 'reserva_ruta',
                'managed': False,
            },
        ),
    ]
