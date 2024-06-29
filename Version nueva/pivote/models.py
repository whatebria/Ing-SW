from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.email



class Preguntas(models.Model):
    enunciado = models.CharField(max_length=500)
    opcionA = models.CharField(max_length=50, null=True, blank=True)   
    opcionB = models.CharField(max_length=50, null=True, blank=True)   
    opcionC = models.CharField(max_length=50, null=True, blank=True)   
    opcionD = models.CharField(max_length=50, null=True, blank=True)   
