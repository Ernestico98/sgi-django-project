# Generated by Django 3.1 on 2020-09-19 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sgi', '0003_auto_20200919_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='medio',
            name='d_devolucion',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='medio',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prestamos', to='sgi.user'),
        ),
        migrations.DeleteModel(
            name='Prestamo',
        ),
    ]