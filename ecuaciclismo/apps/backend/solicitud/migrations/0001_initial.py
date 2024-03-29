# Generated by Django 3.2.6 on 2023-08-04 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lugar', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('ultimo_cambio', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(max_length=100, null=True)),
                ('estado', models.CharField(max_length=50)),
                ('motivo_rechazo', models.CharField(blank=True, max_length=200, null=True)),
                ('path_Pdf', models.TextField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SolicitudRegistroMiembro',
            fields=[
                ('solicitud_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='solicitud.solicitud')),
                ('cedula', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('ciudad', models.CharField(max_length=50)),
                ('ocupacion', models.CharField(max_length=50)),
                ('seguro_medico', models.CharField(max_length=100)),
                ('tipo_sangre', models.CharField(max_length=50)),
                ('contacto_emergencia', models.CharField(max_length=50)),
                ('comprobante', models.TextField(null=True)),
                ('foto_cedula', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('solicitud.solicitud',),
        ),
        migrations.CreateModel(
            name='SolicitudVerificado',
            fields=[
                ('solicitud_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='solicitud.solicitud')),
                ('descripcion', models.TextField()),
                ('imagen', models.TextField()),
                ('usuarios', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('solicitud.solicitud',),
        ),
        migrations.CreateModel(
            name='SolicitudLugar',
            fields=[
                ('solicitud_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='solicitud.solicitud')),
                ('lugar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lugar.lugar')),
            ],
            options={
                'abstract': False,
            },
            bases=('solicitud.solicitud',),
        ),
    ]
