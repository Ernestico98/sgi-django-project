from django.db import models
from django.contrib.auth.models import User as usr


class Centro(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Grupo_Investigacion(models.Model):
    nombg = models.CharField(max_length=100, unique=True)
    centro = models.ForeignKey(Centro, related_name='grupos', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombg


class User(usr):
    CI = models.PositiveBigIntegerField(unique=True)
    address = models.CharField(max_length=100)
    grupo = models.ForeignKey(Grupo_Investigacion, related_name='users', on_delete=models.CASCADE, null=True)
    f_ingreso = models.DateTimeField(null=True)
    roles = [
        ('', ''),
        ('admin', 'Administrator'),
        ('jefe', 'Group Chief'),
        ('user', 'Group Member'),
    ]
    user_role = models.CharField(
        max_length=8,
        choices=roles
    )
    def grupo_pk(self):
        return self.grupo.pk


class Salon(models.Model):
    nombs = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombs


class Medio(models.Model):
    INV = models.CharField(max_length=20, unique='True')
    descripcion = models.CharField(max_length=100)
    garantia = models.BooleanField()
    prestado = models.BooleanField(default=False)
    f_entrada = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=11, decimal_places=2)
    salon = models.ForeignKey(Salon, related_name='medios', on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo_Investigacion, related_name='medios', on_delete=models.CASCADE)

    def __str__(self):
        return self.INV


class Prestamo(models.Model):
    user = models.ForeignKey(User, related_name='prestamos', on_delete=models.CASCADE)
    medio = models.OneToOneField(Medio, related_name='prestamo', on_delete=models.CASCADE)
    f_devolucion = models.DateTimeField()

    def __str__(self):
        return str(self.user.CI) + '  <->  ' + self.medio.INV