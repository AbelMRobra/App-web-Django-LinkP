# Generated by Django 3.0.4 on 2021-01-04 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0018_auto_20201217_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyectos',
            name='fecha_i',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de inicio'),
        ),
    ]