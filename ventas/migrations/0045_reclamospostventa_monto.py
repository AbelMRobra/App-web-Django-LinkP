# Generated by Django 3.2.5 on 2022-02-04 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0044_alter_formulariosolucionpostventa_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='reclamospostventa',
            name='monto',
            field=models.FloatField(default=0, verbose_name='Monto del reclamo'),
        ),
    ]
