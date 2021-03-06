# Generated by Django 3.1 on 2020-09-19 03:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Centro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo_Investigacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombg', models.CharField(max_length=100, unique=True)),
                ('centro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grupos', to='sgi.centro')),
            ],
        ),
        migrations.CreateModel(
            name='Medio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('INV', models.CharField(max_length=20, unique='True')),
                ('descripcion', models.CharField(max_length=100)),
                ('garantia', models.BooleanField()),
                ('prestado', models.BooleanField(null=True)),
                ('f_entrada', models.DateTimeField(auto_now_add=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=11)),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medios', to='sgi.grupo_investigacion')),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CI', models.PositiveBigIntegerField(unique=True)),
                ('nomp', models.CharField(max_length=100)),
                ('dir', models.CharField(max_length=100)),
                ('grupos', models.ManyToManyField(related_name='personas', to='sgi.Grupo_Investigacion')),
            ],
        ),
        migrations.CreateModel(
            name='Salon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombs', models.CharField(max_length=100, unique=True)),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salones', to='sgi.grupo_investigacion')),
            ],
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_devolucion', models.DateTimeField()),
                ('medio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestamos', to='sgi.medio')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestamos', to='sgi.persona')),
            ],
        ),
        migrations.AddField(
            model_name='medio',
            name='salon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medios', to='sgi.salon'),
        ),
    ]
