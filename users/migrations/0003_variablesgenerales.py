# Generated by Django 3.2.5 on 2022-02-15 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_actividadesusuarios'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariablesGenerales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_minimo', models.FloatField(default=0, verbose_name='Valor minimo a autorizar por gerentes')),
            ],
            options={
                'verbose_name': 'Variable general',
                'verbose_name_plural': 'Variables generales',
            },
        ),
    ]
