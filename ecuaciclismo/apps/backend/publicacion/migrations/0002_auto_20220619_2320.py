# Generated by Django 3.2.6 on 2022-06-19 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentariopublicacion',
            name='token',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='detallearchivopublicacion',
            name='token',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='detalleetiquetapublicacion',
            name='token',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='publicacion',
            name='token',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
