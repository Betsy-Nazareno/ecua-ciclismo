# Generated by Django 3.2.6 on 2022-07-26 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruta', '0005_alter_archivo_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivo',
            name='path',
            field=models.TextField(null=True),
        ),
    ]
