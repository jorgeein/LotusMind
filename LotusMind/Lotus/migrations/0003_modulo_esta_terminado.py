# Generated by Django 4.1.7 on 2023-05-06 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lotus', '0002_modulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulo',
            name='esta_terminado',
            field=models.BooleanField(default=False),
        ),
    ]
