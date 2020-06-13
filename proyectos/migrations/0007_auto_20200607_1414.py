# Generated by Django 3.0.4 on 2020-06-07 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0006_proyectos_desde'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unidades',
            name='asig',
            field=models.CharField(choices=[('PROYECTO', 'Proyecto'), ('TERRENO', 'Hon Terreno'), ('HON. LINK', 'Hon Link')], max_length=20, verbose_name='Asignacion'),
        ),
    ]