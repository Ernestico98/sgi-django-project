# Generated by Django 3.1 on 2020-09-22 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgi', '0011_auto_20200922_0343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medio',
            name='f_entrada',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='f_devolucion',
            field=models.DateTimeField(),
        ),
    ]
