
from django.forms import ModelForm
from django import forms
from .models import Consulta



class FormCrearConsulta(ModelForm):
    class Meta:
       model = Consulta
       fields = ['proyecto','cliente','tipologia2','fecha','medio_contacto']

       widgets = {
            'tipologia2': forms.CheckboxSelectMultiple,
            'fecha':forms.SelectDateWidget
        }
    def __init__(self, *args, **kwargs):
        super(FormCrearConsulta, self).__init__(*args, **kwargs)
        self.fields['fecha'].widget.attrs.update({'class' : 'form-control'})
        self.fields['tipologia2'].widget.attrs.update({'class' : ''})
