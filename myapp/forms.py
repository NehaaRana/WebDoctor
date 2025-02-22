from django import forms
from . models import patientRegister
from .models import doctorRegister

class patientForm(forms.ModelForm):
  class Meta:
    model = patientRegister
    fields =[ 'name' ,'email','phno','password' ]


# class doctorForm(forms.ModelForm):
#   class Meta:
#      model = doctorRegister
#      fields =[ 'name' ,'gender','clinic_name','clinic_address','email','phno','password' ]


class doctorForm(forms.ModelForm):
    class Meta:
        model = doctorRegister
        fields = ['name', 'gender', 'clinic_name', 'clinic_address', 'email', 'phno', 'password']


