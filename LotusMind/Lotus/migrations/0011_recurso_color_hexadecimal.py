# Generated by Django 4.1.7 on 2023-05-11 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lotus', '0010_alter_recurso_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurso',
            name='color_hexadecimal',
            field=models.CharField(default=' #FF0000', help_text='Color en formato hexadecimal (#RRGGBB)', max_length=7),
        ),
    ]