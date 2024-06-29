from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.email



class Preguntas(models.Model):
    Id = models.IntegerField
    Enunciado = models.CharField(max_length=500)
    Tipo = models.CharField(max_length=100)
    Respuesta = models.CharField(max_length=128)
    
