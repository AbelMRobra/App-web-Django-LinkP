# Generated by Django 3.2.5 on 2021-07-15 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0038_auto_20210708_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuentacorriente',
            name='flujo_boleto',
            field=models.TextField(blank=True, null=True, verbose_name='Flujo en M3'),
        ),
    ]
