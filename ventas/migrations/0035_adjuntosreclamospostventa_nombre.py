# Generated by Django 3.2.5 on 2021-09-29 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0034_auto_20210929_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='adjuntosreclamospostventa',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre del archivo'),
        ),
    ]