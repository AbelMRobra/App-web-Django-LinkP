# Generated by Django 3.0.4 on 2020-09-29 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0015_comparativas_fecha_autorizacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='comparativas',
            name='visto',
            field=models.CharField(blank=True, choices=[('VISTO', 'Visto'), ('NO_VISTO', 'No Visto'), ('VISTO NO CONFORME', 'No Conforme')], default='NO_VISTO', editable=False, max_length=20, null=True, verbose_name='Revisado por SP'),
        ),
    ]
