# Generated by Django 3.0.4 on 2020-09-28 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0011_auto_20200928_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='almacenero',
            name='ingreso_ventas_link',
            field=models.FloatField(blank=True, null=True, verbose_name='Ingreso por unidades a vender de LINK'),
        ),
        migrations.AddField(
            model_name='almacenero',
            name='pendiente_iibb_tem_link',
            field=models.FloatField(blank=True, null=True, verbose_name='Cuotas a cobrar de LINK'),
        ),
        migrations.AlterField(
            model_name='registroalmacenero',
            name='pendiente_iibb_tem_link',
            field=models.FloatField(blank=True, null=True, verbose_name='Cuotas a cobrar de LINK'),
        ),
    ]
