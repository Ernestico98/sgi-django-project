# Generated by Django 3.1 on 2020-09-20 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgi', '0005_user_f_ingreso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='f_ingreso',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
