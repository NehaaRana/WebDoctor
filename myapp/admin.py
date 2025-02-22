from django.contrib import admin
from .models import patientRegister
from .models import doctorRegister
# Register your models here.

admin.site.register(patientRegister)
admin.site.register(doctorRegister)
