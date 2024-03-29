# Generated by Django 3.2.6 on 2023-11-20 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bicicleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(blank=True, max_length=50)),
                ('marca', models.CharField(blank=True, max_length=100)),
                ('codigo', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PropietarioBicicleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bicicleta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bicicleta.bicicleta')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ImagenBicicleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen_url', models.URLField()),
                ('bicicleta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='bicicleta.bicicleta')),
            ],
        ),
    ]
