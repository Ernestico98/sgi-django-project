# Generated by Django 3.1 on 2020-09-20 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgi', '0006_auto_20200920_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='f_ingreso',
            field=models.DateTimeField(null=True),
        ),
    ]
