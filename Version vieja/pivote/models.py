from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.email
TIPOS = (
    ('--', '-----'),
    ('De', 'Desarrollo'),
    ('SM', 'Seleccion Multiple'),
    )

class Test(models.Model):#survey
    titulo = models.CharField(max_length=200, null=True)
    descripcion = models.TextField(null=True)

class Pregunta(models.Model):#question
    test = models.ForeignKey(Test, related_name='preguntas', on_delete=models.CASCADE)
    enunciado = models.CharField(max_length=500)
    tipo = models.CharField(max_length=20, choices=TIPOS)

class Tipo(models.Model):#choice
    pregunta = models.ForeignKey(Pregunta, related_name='tiposPreguntas', on_delete=models.CASCADE)
    textOpcion = models.CharField(max_length=200)
    def __str__(self):
        return self.textOpcion

class Responde(models.Model):#response
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    estudiante = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    creado_el = models.DateField(auto_now_add=True)
    def __str__(self):
        return f'Respuestas de {self.estudiante} a {self.test}'
    
class Respuesta(models.Model):#answer
    respuesta = models.ForeignKey(Responde, related_name='respuestas', on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto = models.TextField(blank=True, null=True)
    tipos = models.ForeignKey(Tipo, blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'Respuesta a {self.pregunta} por {self.respuesta.estudiante}'