# Generated by Django 3.2.6 on 2022-08-20 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0005_auto_20220820_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleusuario',
            name='bicicleta',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='usuario.bicicleta'),
        ),
    ]
