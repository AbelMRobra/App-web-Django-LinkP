# Generated by Django 3.2.5 on 2021-08-17 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0043_registroemail'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuentacorriente',
            name='estado',
            field=models.CharField(choices=[('activo', 'Activo'), ('baja', 'Baja')], default='activo', max_length=20, verbose_name='Estado'),
        ),
    ]
