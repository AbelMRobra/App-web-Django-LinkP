# Generated by Django 3.0.4 on 2020-11-06 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0004_notadepedido'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notadepedido',
            options={'verbose_name': 'Correspondencia', 'verbose_name_plural': 'Correspondencias'},
        ),
        migrations.AddField(
            model_name='notadepedido',
            name='tipo',
            field=models.CharField(blank=True, choices=[('NP', 'Np'), ('OS', 'Os')], max_length=20, null=True, verbose_name='Tipo de correspondencia'),
        ),
        migrations.AddField(
            model_name='notadepedido',
            name='visto',
            field=models.IntegerField(blank=True, null=True, verbose_name='Visto'),
        ),
        migrations.AlterField(
            model_name='notadepedido',
            name='fecha_requerida',
            field=models.CharField(max_length=200, verbose_name='Fecha requerida'),
        ),
        migrations.AlterField(
            model_name='notadepedido',
            name='numero',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nota de pedido numero'),
        ),
    ]
