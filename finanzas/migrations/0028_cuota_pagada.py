# Generated by Django 3.0.4 on 2021-04-15 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0027_auto_20210323_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuota',
            name='pagada',
            field=models.CharField(choices=[('SI', 'Si'), ('NO', 'No')], default='NO', max_length=20, verbose_name='Pagada'),
        ),
    ]
