# Generated by Django 3.0.4 on 2020-08-05 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0007_registroalmacenero'),
    ]

    operations = [
        migrations.AddField(
            model_name='registroalmacenero',
            name='fecha',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de guardado'),
        ),
    ]
