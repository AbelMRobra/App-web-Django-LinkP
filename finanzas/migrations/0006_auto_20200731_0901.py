# Generated by Django 3.0.4 on 2020-07-31 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0005_cuota_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuota',
            name='concepto',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Concepto'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='documento_1',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Documento 1'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='documento_2',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Documento 2'),
        ),
    ]