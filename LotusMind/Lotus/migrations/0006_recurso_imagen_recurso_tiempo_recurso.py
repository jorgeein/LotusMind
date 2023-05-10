# Generated by Django 4.1.7 on 2023-05-09 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lotus', '0005_usuario_historial_modulos'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurso',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='frontend/static/frontend/figuras'),
        ),
        migrations.AddField(
            model_name='recurso',
            name='tiempo_recurso',
            field=models.IntegerField(default=3),
        ),
    ]
