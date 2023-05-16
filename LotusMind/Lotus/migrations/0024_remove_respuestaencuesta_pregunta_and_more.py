# Generated by Django 4.1.7 on 2023-05-15 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Lotus', '0023_pregunta_alter_recurso_tipo_respuestaencuesta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='respuestaencuesta',
            name='pregunta',
        ),
        migrations.RemoveField(
            model_name='respuestaencuesta',
            name='respuesta',
        ),
        migrations.AddField(
            model_name='pregunta',
            name='respuesta',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='RespuestaPreguntaEncuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta', models.IntegerField()),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Lotus.pregunta')),
                ('respuesta_encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Lotus.respuestaencuesta')),
            ],
        ),
        migrations.AddField(
            model_name='respuestaencuesta',
            name='preguntas',
            field=models.ManyToManyField(through='Lotus.RespuestaPreguntaEncuesta', to='Lotus.pregunta'),
        ),
    ]
