# Generated by Django 3.2.5 on 2021-07-16 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0029_auto_20210625_1446'),
        ('rrhh', '0048_archivosgenerales'),
        ('crm', '0002_consulta_adjunto_propuesta'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='proyecto_no_est',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='medio_contacto',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Medio de contacto'),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='proyecto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyectos.proyectos'),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rrhh.datosusuario'),
        ),
    ]
