# Generated by Django 3.2.6 on 2024-12-31 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consejo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('icono', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'consejos_negocios',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=200)),
                ('detalle', models.TextField()),
                ('imagen', models.URLField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tip_consejo',
                'managed': False,
            },
        ),
    ]
