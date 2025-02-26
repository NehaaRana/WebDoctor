from django import forms
from . models import patientRegister,doctorRegister,appointment
from django.core.exceptions import ValidationError
from datetime import datetime, time, timedelta

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


 
class appointmentForm(forms.ModelForm):
    class Meta:
       model=appointment
       fields = ['appointment_date', 'appointment_time', 'reason','symptoms'] 
       
    def clean_appointment_date(self):
        appointment_date  = self.cleaned_data.get('appointment_date')
        today = datetime.now().date()
        if appointment_date < today:
            raise ValidationError("Appointment date cannot be in the past.")
        return appointment_date


    def clean_appointment_time(self):
        appointment_time = self.cleaned_data.get('appointment_time')
        start_time = time(9, 0)  # 9:00 AM
        end_time = time(17, 0)   # 5:00 PM

        if not (start_time <= appointment_time <= end_time):
            raise ValidationError("Appointment time must be between 09:00 AM and 05:00 PM.")
        return appointment_time
    
   

    # def clean_status(self):
    #     status = self.cleaned_data.get('status')
    #     valid_statuses = ['pending', 'confirmed', 'cancelled']
    #     if status not in valid_statuses:
    #         raise ValidationError(f"Status must be one of the following: {', '.join(valid_statuses)}.")
    #     return status




