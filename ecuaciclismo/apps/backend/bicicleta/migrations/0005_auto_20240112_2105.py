# Generated by Django 3.2.6 on 2024-01-12 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bicicleta', '0004_alter_bicicleta_codigo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bicicleta',
            name='tipo',
        ),
        migrations.AddField(
            model_name='bicicleta',
            name='color',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='bicicleta',
            name='factura',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='bicicleta',
            name='modadlidad',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='bicicleta',
            name='modelo',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='bicicleta',
            name='n_serie',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='bicicleta',
            name='tienda_origen',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='bicicleta',
            name='codigo',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='bicicleta',
            name='marca',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
