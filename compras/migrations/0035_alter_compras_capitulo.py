# Generated by Django 3.2.5 on 2022-02-28 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestos', '0039_auto_20220217_1409'),
        ('compras', '0034_comparativas_quien_autorizo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compras',
            name='capitulo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='presupuestos.capitulos'),
        ),
    ]
