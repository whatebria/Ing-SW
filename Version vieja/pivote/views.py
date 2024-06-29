from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, FormPreguntas, FormTipo
from .models import User, Test, Pregunta, Tipo, Responde, Respuesta
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

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


def crearTest(request):
    if request.method == 'POST':
        test = Test.objects.create(titulo = request.POST.get('titulo'), descripcion = request.POST.get('descripcion')) 
        return redirect('crear_preguntas', test_id=test.id)
    return render(request, 'pivote/creacionTest.html')

def crear_preguntas(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    numPreguntas = test.preguntas.count()
    PreguntaFormSet = modelformset_factory(Pregunta, form=FormPreguntas, extra=3)
    TipoFormSet = modelformset_factory(Tipo, form=FormTipo, extra=3)

    if request.method == 'POST':
        pregunta_formset = PreguntaFormSet(request.POST, queryset=Pregunta.objects.filter(test=test))
        tipo_formset = TipoFormSet(request.POST) 
        if pregunta_formset.is_valid() and tipo_formset.is_valid():
            preguntas = pregunta_formset.save(commit=False)
            for pregunta in preguntas:
                pregunta.test = test
                pregunta.save()
            tipos = tipo_formset.save(commit=False)
            for tipo in tipos:
                tipo.pregunta = pregunta
                tipo.save()
            return redirect('testList')
    else:
        pregunta_formset = PreguntaFormSet(queryset=Pregunta.objects.filter(test=test))
        tipo_formset = TipoFormSet(queryset=Tipo.objects.none())

    context = {
        'test': test,
        'preguntas_formset': pregunta_formset,
        'tipos_formset': tipo_formset
    }
    return render(request, 'pivote/preguntas.html', context)

def tomarTest(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    preguntas = test.preguntas.all()
    if request.method == 'POST':
        respuesta = Respuesta.objects.create(test=test, estudiante=request.user)
        for pregunta in preguntas:
            respuestaTexto = request.POST.get(f'respuesta_{respuesta.id}')
            if pregunta.tipo == 'Desarrollo':
                Pregunta.objects.create(respuestaTexto=respuesta, pregunta=pregunta, enunciado=respuestaTexto)
            elif pregunta.tipo == 'Seleccion Multiple':
                tipo_ids = request.POST.gestlist(f'pregunta_{pregunta.id}')
                for tipo_id in tipo_ids:
                    tipo = Tipo.objects.get(id=tipo_id)
                    Respuesta.objects.create(respuesta=respuesta, pregunta=pregunta, tipo=tipo)
        return redirect('testList')
    
    return render(request, 'pivote/tomarTest.html', {'test': test, 'preguntas': preguntas})