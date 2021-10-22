# Generated by Django 3.2.5 on 2021-10-19 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0056_alter_cajas_usuarios_visibles'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActividadesUsuarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=30, verbose_name='Categoria')),
                ('accion', models.CharField(max_length=50, verbose_name='Acción')),
                ('momento', models.DateTimeField(verbose_name='Fecha')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.datosusuario', verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Actividad',
                'verbose_name_plural': 'Actividades',
            },
        ),
    ]
