# Generated by Django 3.2.6 on 2022-07-31 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ruta', '0006_archivo_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordenada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('ultimo_cambio', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(max_length=100, null=True)),
                ('latitud', models.TextField()),
                ('longitud', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Requisito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('ultimo_cambio', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(max_length=100, null=True)),
                ('nombre', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='etiquetaruta',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='ubicacion',
            name='latitud',
        ),
        migrations.RemoveField(
            model_name='ubicacion',
            name='longitud',
        ),
        migrations.AddField(
            model_name='ruta',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ruta',
            name='estimado_tiempo',
            field=models.IntegerField(null=True),
        ),
        migrations.CreateModel(
            name='DetalleRequisito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('ultimo_cambio', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(max_length=100, null=True)),
                ('requisito', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ruta.requisito')),
                ('ruta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ruta.ruta')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='ubicacion',
            name='coordenada_x',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='x_coordenada', to='ruta.coordenada'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ubicacion',
            name='coordenada_y',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='y_coordenada', to='ruta.coordenada'),
            preserve_default=False,
        ),
    ]
