# Generated by Django 3.0.4 on 2021-03-23 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0027_datosusuario_fecha_ingreso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosusuario',
            name='nombre',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre, Apellido'),
        ),
    ]
