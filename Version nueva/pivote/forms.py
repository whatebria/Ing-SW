from django import forms
from .models import User, Preguntas


# permite crear formularios basados en modelos de la base de datos.
class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'name': 'Nombre',
            'email': 'Correo',
            'password': 'Contraseña',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if User.objects.filter(name=name).exists():
            raise forms.ValidationError("Un usuario ya está registrado con este nombre.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un usuario ya está registrado con este correo electrónico.")
        return email

    def clean_password(self):
        minuscula = False
        mayuscula = False
        numero = False
        password = self.cleaned_data.get('password')
        name = self.cleaned_data.get('name')
        if len(password) < 6 :
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        for minus in password:
            if minus.islower()== True:
                minuscula = True
        if not minuscula:
            raise forms.ValidationError("La contraseña debe tener al menos una minuscula.")
        for mayus in password:
            if mayus.isupper()==True:
                mayuscula = True
        if not mayuscula:
            raise forms.ValidationError("La contraseña debe tener al menos una mayuscula.")
        for num in password:
            if num.isdigit()==True:
                numero=True
        if not numero:
            raise forms.ValidationError("La contraseña debe tener al menos un numero.")
        if password.count(name):
            raise forms.ValidationError("La contraseña no debe coincidir con su nombre.")
        return password

TIPOS = (
    ('--', '-----'),
    ('De', 'Desarrollo'),
    ('SM', 'Seleccion Multiple'),
    ('Ot', 'Otro'),
    )

class FormPreguntas(forms.ModelForm):
    class Meta:
        model = Preguntas
        fields = (
            'id', 'Enunciado', 'Tipo', 'Respuesta'
        )
        widgets = {
            'Enunciado': forms.TextInput(attrs={'class': 'form-control'}),
            'Tipo': forms.Select(choices=TIPOS, attrs={'class': 'form-control'}),
            'Respuesta': forms.TextInput(attrs={'class': 'form-control'})
        }

