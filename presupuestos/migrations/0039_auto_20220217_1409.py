# Generated by Django 3.2.5 on 2022-02-17 17:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestos', '0038_presupuestos_consumption_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulos',
            name='valor',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='modelopresupuesto',
            name='cantidad',
            field=models.FloatField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Cantidad'),
        ),
    ]