# Generated by Django 3.1 on 2020-09-22 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgi', '0010_auto_20200921_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medio',
            name='f_entrada',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='f_devolucion',
            field=models.DateField(),
        ),
    ]