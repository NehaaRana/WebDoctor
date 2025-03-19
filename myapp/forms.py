from django import forms
from . models import patientRegister,doctorRegister,appointment,Payment,review
from django.core.exceptions import ValidationError
from datetime import datetime, time, timedelta
from .models import adminLogin
from . models import patientRegister,doctorRegister,appointment,Payment,HealthRecord,Prescription,ConsultationReport
from django.core.exceptions import ValidationError
from datetime import datetime, time, timedelta

class patientForm(forms.ModelForm):
  class Meta:
    model = patientRegister
    fields =[ 'name' ,'email','phno','password' ]


class doctorForm(forms.ModelForm):
    class Meta:
        model = doctorRegister
        fields = ['name', 'gender', 'qualification', 'specialization', 'email', 'phno', 'password']


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

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_status', 'payment_method']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = review
        fields = ["rating", "review_text"]

class adminForm(forms.ModelForm):
    class Meta:
       model = adminLogin
       fields = ['username','email','password']
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
    
   
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_status', 'payment_method']

# class HealthRecordForm(forms.ModelForm):
#     class Meta:
#         model = HealthRecord
#         fields = ['bp_systolic', 'bp_diastolic', 'sugar_level', 'weight']


class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = [
            'bp_systolic', 'bp_diastolic', 'heart_rate',  'sugar_level',
            'steps_walked', 'sleep_hours'
        ]
        widgets = {
            'bp_systolic': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Systolic BP (e.g., 120 mmHg)'}),
            'bp_diastolic': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Diastolic BP(e.g., 80 mmHg)'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Heart Rate(e.g., 75 BPM)'}),
            'sugar_level': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Sugar Level(e.g., 90 mg/dL)'}),
            'steps_walked': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Steps Walked(e.g., 8000 steps)'}),
            'sleep_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Sleep Hours(e.g., 8 hours)'}),
        }

# prescription form
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medicines', 'diagnosis', 'instructions']  # Removed 'patient' field
        widgets = {
            'medicines': forms.Textarea(attrs={'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'rows': 2}),
            'instructions': forms.Textarea(attrs={'rows': 3}),
        }

# Auto-generated Report
class ConsultationReportForm(forms.ModelForm):
    class Meta:
        model = ConsultationReport
        fields = ['diagnosis', 'prescription', 'notes']