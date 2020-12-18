# Generated by Django 3.0.4 on 2020-12-17 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0024_auto_20201209_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='almacenero',
            name='financiacion',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Recargo por financiacion'),
        ),
        migrations.AddField(
            model_name='almacenero',
            name='tenencia',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Resultado por tenencia'),
        ),
        migrations.AddField(
            model_name='registroalmacenero',
            name='financiacion',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Recargo por financiacion'),
        ),
        migrations.AddField(
            model_name='registroalmacenero',
            name='tenencia',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Resultado por tenencia'),
        ),
    ]
