from django.shortcuts import render
from .forms import UserRegistrationForm, FormPreguntas
from .models import Preguntas

def home(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'pivote/home.html', {'form': form, 'message': '¡Usuario registrado correctamente!'})
    else:
        form = UserRegistrationForm()
    return render(request, 'pivote/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'pivote/home.html', {'form': form, 'message': 'Registro exitoso, por favor verifica tu correo'})
    else:
        form = UserRegistrationForm()
    return render(request, 'pivote/home.html', {'form': form})

def test(request):
    context = {'form': FormPreguntas, 
               'test': Preguntas.objects.all()
               }
    return render(request, 'pivote/creacionTest.html', context)

def create_pregunta(request):
    if request.method == 'POST':
        form = FormPreguntas(request.POST or None)
        if form.is_valid():
            test = form.save()
            context = {'test': test}
            return render(request, 'pivote/verTest.html', context)

    return render(request, 'pivote/preguntas.html', {'form': FormPreguntas})

def verTest(request):
    context = {'form': FormPreguntas, 
               'test': Preguntas.objects.all()
               }
    return render(request, 'pivote/verTest.html', context)