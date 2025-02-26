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


class passwordChangeForm(forms.Form):
    old_password = forms.CharField()
    new_password = forms.CharField()
    confirm_password = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Old password is incorrect.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")
        return cleaned_data

 


