# Generated by Django 3.2.5 on 2021-07-20 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0048_archivosgenerales'),
        ('finanzas', '0042_cuentacorriente_flujo_boleto_m3'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistroEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('estado_cuenta', models.FileField(upload_to='media')),
                ('destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finanzas.cuentacorriente')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.datosusuario')),
            ],
        ),
    ]