# Generated by Django 3.2.5 on 2021-11-23 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0029_alter_proveedores_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedores',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
    ]
