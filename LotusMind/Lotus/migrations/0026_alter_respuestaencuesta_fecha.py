# Generated by Django 4.1.7 on 2023-05-17 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lotus', '0025_respuestaencuesta_completada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respuestaencuesta',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
