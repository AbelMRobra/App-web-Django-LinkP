# Generated by Django 3.2.5 on 2021-12-23 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestos', '0032_auto_20211124_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='bitacoras',
            name='hashtag',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Hashtag'),
        ),
    ]
