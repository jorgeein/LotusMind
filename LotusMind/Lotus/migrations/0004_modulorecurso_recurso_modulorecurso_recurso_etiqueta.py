# Generated by Django 4.1.7 on 2023-05-09 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Lotus', '0003_modulo_esta_terminado'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuloRecurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Lotus.modulo')),
            ],
        ),
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_rec', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('Video', 'Video'), ('Musica', 'Música'), ('Libro', 'Libro'), ('Orientacion Educativa', 'Orientacion Educativa'), ('Curso', 'Curso'), ('MEDITACION', 'Meditacion')], default='Video', max_length=30)),
                ('descripcion', models.TextField()),
                ('cant_temas', models.IntegerField(blank=True, null=True)),
                ('modulos', models.ManyToManyField(through='Lotus.ModuloRecurso', to='Lotus.modulo')),
            ],
        ),
        migrations.AddField(
            model_name='modulorecurso',
            name='recurso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Lotus.recurso'),
        ),
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('modulos', models.ManyToManyField(to='Lotus.modulo')),
                ('recursos', models.ManyToManyField(to='Lotus.recurso')),
            ],
        ),
    ]
