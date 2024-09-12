from django.db import models
from django.db.models import Model
from django.utils import timezone


# Create your models here.

class Cliente(models.Model):
    id= models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=150)
    apellido= models.CharField(max_length=150)
    telefono= models.CharField(max_length=150)
    email= models.EmailField(unique=True)
    def __str__(self) -> str:
        return self.nombre

class Mesa(models.Model):
    id= models.AutoField(primary_key=True)
    numero= models.CharField(max_length=150)
    capacidad= models.IntegerField()
    ubicacion= models.CharField(max_length=150)
    def __str__(self) -> str:
        return self.numero

class Reservacion(models.Model):
    ESTADO_CHOICES=[
        ("pendiente", "pendiente"),
        ("confirmada", "confirmada"),
        ("cancelada", "cancelada"),
    ]
    id= models.AutoField(primary_key=True)
    cliente= models.ForeignKey("Cliente", on_delete=models.CASCADE)
    mesa= models.ForeignKey("Mesa", on_delete=models.CASCADE)
    fecha_orden= models.DateTimeField(null=True, blank=False)
    duracion= models.DurationField()
    estado= models.CharField(choices=ESTADO_CHOICES, max_length=150)
    def __str__(self) -> str:
        return self.cliente


class Plato(models.Model):
    id= models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=150)
    descripcion= models.TextField(max_length=150)
    precio= models.DecimalField(max_digits=8,decimal_places=2)
    def __str__(self) -> str:
        return self.nombre


class Menu(models.Model):
    id= models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=150)
    platos= models.ManyToManyField(Plato, blank=True,related_name='menus')
    fecha_disponible= models.DateField(null=True, blank=False)
    def __str__(self) -> str:
        return self.nombre
