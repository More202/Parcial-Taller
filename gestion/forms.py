from django import forms
from .models import *


class Clienteform(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class Mesaform(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = '__all__'

class Reservacionform(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = '__all__'
        widgets = {
            'fecha_orden': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'duracion': forms.TimeInput(attrs={'type': 'time', 'step': '1800'}),  
        }
class Platoform(forms.ModelForm):
    class Meta:
        model = Plato
        fields = '__all__'

class Menuform(forms.ModelForm):
    platos = forms.ModelMultipleChoiceField(
        queryset=Plato.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Menu
        fields = ['nombre', 'platos', 'fecha_disponible']
        widgets = {
            'fecha_disponible': forms.DateInput(attrs={'type': 'date'}),
        }