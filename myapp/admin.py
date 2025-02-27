from django.contrib import admin
from .models import patientRegister
from .models import doctorRegister,appointment,review,Payment
# Register your models here.

admin.site.register(patientRegister)
admin.site.register(doctorRegister)
admin.site.register(appointment)
admin.site.register(review)
admin.site.register(Payment)
