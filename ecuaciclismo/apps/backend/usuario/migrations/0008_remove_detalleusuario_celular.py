# Generated by Django 3.2.6 on 2022-08-20 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0007_auto_20220820_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalleusuario',
            name='celular',
        ),
    ]
