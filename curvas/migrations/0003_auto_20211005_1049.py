# Generated by Django 3.1.6 on 2021-10-05 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestos', '0031_documentacionproyectopresupuesto'),
        ('proyectos', '0031_proyectos_google_maps'),
        ('curvas', '0002_alter_partidascapitulos_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='partidascapitulos',
            name='fecha_f_aplicacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha final de aplicacion'),
        ),
        migrations.AddField(
            model_name='partidascapitulos',
            name='fecha_i_aplicacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha inicial de aplicacion'),
        ),
        migrations.AlterField(
            model_name='partidascapitulos',
            name='capitulo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='presupuestos.capitulos'),
        ),
        migrations.AlterField(
            model_name='partidascapitulos',
            name='proyecto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='proyectos.proyectos'),
        ),
    ]
