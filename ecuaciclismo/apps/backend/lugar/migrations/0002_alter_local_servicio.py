# Generated by Django 3.2.6 on 2023-08-06 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lugar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='local',
            name='servicio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lugar.servicio'),
        ),
    ]