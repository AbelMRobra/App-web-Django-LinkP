# Generated by Django 3.2.5 on 2021-07-30 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestos', '0027_articulos_tipo_articulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='prametros',
            name='iva',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='IVA'),
        ),
        migrations.AlterField(
            model_name='prametros',
            name='comer',
            field=models.FloatField(default=0, verbose_name='Honorarios Comercialización'),
        ),
        migrations.AlterField(
            model_name='prametros',
            name='ganancia',
            field=models.FloatField(default=0, verbose_name='Ganancia'),
        ),
        migrations.AlterField(
            model_name='prametros',
            name='imprevitso',
            field=models.FloatField(default=0, verbose_name='Imprevisto'),
        ),
        migrations.AlterField(
            model_name='prametros',
            name='link',
            field=models.FloatField(default=0, verbose_name='Honorarios Desarrolladora'),
        ),
        migrations.AlterField(
            model_name='prametros',
            name='por_comer',
            field=models.FloatField(default=0, verbose_name='Porcentaje aplicación comercialización'),
        ),
        migrations.AlterField(
            model_name='prametros',
            name='por_temiibb',
            field=models.FloatField(default=0, verbose_name='Porcentaje de aplicación TEM e IIBB'),
        ),
        migrations.AlterField(
            model_name='prametros',
            name='soft',
            field=models.FloatField(default=0, verbose_name='Soft'),
        ),
        migrations.AlterField(
            model_name='prametros',
            name='tasa_des',
            field=models.FloatField(default=0, verbose_name='Tasa descuento'),
        ),
        migrations.AlterField(
            model_name='prametros',
            name='tasa_des_p',
            field=models.FloatField(default=0, verbose_name='Tasa de descuento del costo'),
        ),
        migrations.AlterField(
            model_name='prametros',
            name='tem_iibb',
            field=models.FloatField(default=0, verbose_name='TEM e IIBB'),
        ),
        migrations.AlterField(
            model_name='prametros',
            name='terreno',
            field=models.FloatField(default=0, verbose_name='Honorarios Terreno'),
        ),
    ]