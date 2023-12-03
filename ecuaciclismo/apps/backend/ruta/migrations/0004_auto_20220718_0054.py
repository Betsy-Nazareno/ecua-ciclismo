# Generated by Django 3.2.6 on 2022-07-18 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruta', '0003_rename_etiqueta_etiquetaruta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archivo',
            name='extension',
        ),
        migrations.RemoveField(
            model_name='archivo',
            name='nombre',
        ),
        migrations.AddField(
            model_name='archivo',
            name='tipo',
            field=models.CharField(choices=[('AUDIOS', 'audios'), ('FOTOS', 'fotos'), ('ADJUNTOS', 'adjuntos')], default=1, max_length=8),
            preserve_default=False,
        ),
    ]