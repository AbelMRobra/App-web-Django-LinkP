# Generated by Django 3.2.5 on 2021-08-12 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0050_auto_20210804_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='sugerencia',
            name='respuestas',
            field=models.TextField(default='', verbose_name='Respuestas'),
        ),
    ]
