from django import forms
from . models import patientRegister,doctorRegister,appointment
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

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
       fields = ['appointment_date', 'appointment_time', 'reason'] 
       
    def clean_appointment_date(self):
        date = self.cleaned_data.get('appointment_date')
        if date < datetime.today().date():
            raise ValidationError("Appointment date cannot be in the past.")
        return date

    def clean_appointment_time(self):
        time = self.cleaned_data.get('appointment_time')
        start_time = datetime.strptime("09:00", "%H:%M").time()
        end_time = datetime.strptime("17:00", "%H:%M").time()
        if not (start_time <= time <= end_time):
            raise ValidationError("Appointment time must be between 09:00 AM and 05:00 PM.")
        return time
    
    widgets = {
            "appointment_date": forms.DateInput(
                attrs={
                    "class": "form-control datetimepicker",
                    "placeholder": "DD/MM/YYYY",
                    "required": True,
                    "type": "text"  # Set as text so JavaScript can control the format
                }
            ),
            "appointment_time": forms.TextInput(  # Use TextInput for custom formatting
                attrs={
                    "class": "form-control timepicker",
                    "placeholder": "HH:MM AM/PM",
                    "required": True,
                    "type": "text"
                }
            ),
            "reason": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter Your Reason", "rows": 3}),
            "symptoms": forms.TextInput(attrs={"class": "form-control", "placeholder": "Symptoms (Optional)"}),
        }

    # def clean_status(self):
    #     status = self.cleaned_data.get('status')
    #     valid_statuses = ['pending', 'confirmed', 'cancelled']
    #     if status not in valid_statuses:
    #         raise ValidationError(f"Status must be one of the following: {', '.join(valid_statuses)}.")
    #     return status




