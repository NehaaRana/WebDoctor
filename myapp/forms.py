from django import forms
from . models import patientRegister

class patientForm(forms.ModelForm):
  class Meta:
    model = patientRegister
    fields =[ 'name' ,'email','phno','password' ]
