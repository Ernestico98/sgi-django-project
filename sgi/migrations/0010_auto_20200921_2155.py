# Generated by Django 3.1 on 2020-09-21 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgi', '0009_auto_20200921_0236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamo',
            name='f_devolucion',
            field=models.DateTimeField(),
        ),
    ]