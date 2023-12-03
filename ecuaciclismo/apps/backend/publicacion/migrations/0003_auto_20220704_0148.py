# Generated by Django 3.2.6 on 2022-07-04 01:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publicacion', '0002_auto_20220619_2320'),
    ]

    operations = [
        migrations.CreateModel(
            name='EtiquetaPublicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('ultimo_cambio', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(max_length=100, null=True)),
                ('nombre', models.TextField()),
                ('descripcion', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='publicacion',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='detalleetiquetapublicacion',
            name='etiqueta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='publicacion.etiquetapublicacion'),
        ),
    ]