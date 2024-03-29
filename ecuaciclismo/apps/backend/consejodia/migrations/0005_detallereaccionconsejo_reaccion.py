# Generated by Django 3.2.6 on 2022-07-10 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('consejodia', '0004_auto_20220705_0223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reaccion',
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
        migrations.CreateModel(
            name='DetalleReaccionConsejo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('ultimo_cambio', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(max_length=100, null=True)),
                ('consejo_dia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='consejodia.consejodia')),
                ('reaccion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='consejodia.reaccion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
