# Generated by Django 3.0.4 on 2020-06-11 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestos', '0016_auto_20200611_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuestos',
            name='saldo_cap',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Archivo Saldo Capitulo'),
        ),
    ]