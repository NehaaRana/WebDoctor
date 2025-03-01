# import datetime
from datetime import time, timedelta
import datetime
from django.utils import timezone
from pyexpat.errors import messages  # Correct way to use strptime
from django.urls import reverse
from datetime import datetime, timedelta, time, date
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from .forms import patientForm,doctorForm,passwordChangeForm
from .forms import patientForm,doctorForm ,appointmentForm
from .forms import adminForm 
from .models import adminLogin # Assuming an admin model

# from .forms import doctorForm
from .models import patientRegister,doctorRegister
# #####################################
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.shortcuts import get_object_or_404
import json
from .models import appointment,Payment
import os
# Create your views here.
# from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from django.shortcuts import get_object_or_404
from django.utils.timezone import now

# Create your views here.
def home(request):
    # all_patient=patientRegister.objects.all
    articles = [
        {
            "image": "assets/img/blog/blog-11.jpg",
            "title": "PMS – Making your clinic painless visit?",
            "description": "Making your clinic visits stress-free, effortless and enhancing your clinic experience with a painless appointment process.",
            "link": "#highlights"
        },
        {
            "image": "assets/img/blog/blog-12.jpg",
            "title": "What are the benefits of Online Doctor Booking?",
            "description": "Easily book appointments from anywhere, at any time, without the need to visit or call a clinic.",
            "link": "#highlights"
        }
    ]

    work_steps = [
        {
            "icon": "assets/img/icons/work-01.svg",
            "title": "Search Doctor",
            "description": "Easily find and connect with the right doctor for you with a simple click. Discover a wide range of qualified healthcare professionals at your fingertips."
        },

        {
            "icon": "assets/img/icons/work-02.svg",
            "title": "Check Doctor Profile",
            "description": "Explore doctor profiles for comprehensive information on qualifications, specialties, and patient feedback to make informed decisions for personalized healthcare."
        }
     ]
     
    return render(request, "home.html", {"articles": articles, "work_steps": work_steps})

def about_us(request):
    return render(request, 'about-us.html')
def about(request):
    return render(request, 'about.html')

def contact(request):
         return render(request, 'contact.html')

def contact_us(request):
         return render(request, 'contact-us.html')

def register(request):
         return render(request, 'register.html')

# def login(request):
#     email = None
#     password = None
#     user_type = None
#     user = None

#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         user_type = request.POST.get("user_type")
#         # patient=patientRegister.objects.get(email=email,password=password)

#         # doctor = doctorRegister.objects.get(email=email, password=password)  
#         user = None

#         if user_type == "patient":
#             try:
#                 user = patientRegister.objects.get(email=email)
#                 request.session['patient_id'] = user.id
#             except patientRegister.DoesNotExist:
#                 return render(request, "login.html", {"error": "Patient does not exist"})

#         elif user_type == "doctor":
#             try:
#                 user = doctorRegister.objects.get(email=email)
#                 request.session['doctor_id'] = user.id  # Store doctor ID in session
#             except doctorRegister.DoesNotExist:
#                 return render(request, "login.html", {"error": "Doctor does not exist"})

#         else:
#             return render(request, "login.html", {"error": "Invalid user type"})

#         # **Manually check the password**
#         if check_password(password, user.password):  # Securely verify password
#             # Redirect based on user type
#             if user_type == "patient":
#                 return redirect("patient_dashboard")  # Update with actual patient dashboard URL
#             elif user_type == "doctor":
#                 return redirect("doctor_dashboard")  # Update with actual doctor dashboard URL

#         return render(request, "login.html", {"error": "Invalid email or password"})

#     return render(request, "login.html")


# def login(request):
#     email = None
#     password = None
#     user_type = None
#     user = None

#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         user_type = request.POST.get("user_type")
#         # patient=patientRegister.objects.get(email=email,password=password)

#         # doctor = doctorRegister.objects.get(email=email, password=password)  
#         user = None

#         if user_type == "patient":
#             try:
#                 user = patientRegister.objects.get(email=email)
#                 request.session['patient_id'] = user.id
#             except patientRegister.DoesNotExist:
#                 return render(request, "login.html", {"error": "Patient does not exist"})

#         elif user_type == "doctor":
#             try:
#                 user = doctorRegister.objects.get(email=email)
#                 request.session['doctor_id'] = user.id  # Store doctor ID in session
#             except doctorRegister.DoesNotExist:
#                 return render(request, "login.html", {"error": "Doctor does not exist"})

#         else:
#             return render(request, "login.html", {"error": "Invalid user type"})

#         # ✅ **Manually check the password**
#         if check_password(password, user.password):  # Securely verify password
#             # Redirect based on user type
#             if user_type == "patient":
#                 return redirect("patient_dashboard")  # Update with actual patient dashboard URL
#             elif user_type == "doctor":
#                 return redirect("doctor_dashboard")  # Update with actual doctor dashboard URL

#         return render(request, "login.html", {"error": "Invalid email or password"})

#     return render(request, "login.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")
        user = None

        print(f"Login attempt: Email={email}, UserType={user_type}")

        print(f"Login attempt: Email={email}, UserType={user_type}")

        if user_type == "patient":
            try:
                user = patientRegister.objects.get(email=email)
                request.session['patient_id'] = user.id  # Store in session
                print(f"Patient found: {user.email}")
                request.session['patient_id'] = user.id  # Store in session
                print(f"Patient found: {user.email}")
            except patientRegister.DoesNotExist:
                print("Patient does not exist")
                print("Patient does not exist")
                return render(request, "login.html", {"error": "Patient does not exist"})

        elif user_type == "doctor":
            try:
                user = doctorRegister.objects.get(email=email)
                # request.session['doctor_id'] = user.id  # Store in session
                if not user.is_approved:
                    print("Doctor not approved yet")
                    return render(request, "login.html", {"error": "Your account is pending approval. Please wait for admin approval."})

                print(f"Doctor found: {user.email}")
                request.session['doctor_id'] = user.id  # Store doctor ID in session
                
                
            except doctorRegister.DoesNotExist:
                print("Doctor does not exist")
              
                return render(request, "login.html", {"error": "Doctor does not exist"})

        else:
            print("Invalid user type")
            
            return render(request, "login.html", {"error": "Invalid user type"})

        # **Compare hashed password using check_password()**
        print(f"Entered Password: {password}")
        print(f"Stored Hashed Password: {user.password}")

        if check_password(password, user.password):  # Securely verify password
            print("Password matched! Redirecting...")
        # **Compare hashed password using check_password()**
        print(f"Entered Password: {password}")
        print(f"Stored Hashed Password: {user.password}")

        if check_password(password, user.password):  # Securely verify password
            print("Password matched! Redirecting...")
            if user_type == "patient":
                return redirect("patient_dashboard")  
                  
            elif user_type == "doctor":
                return redirect("doctor_dashboard")  
            else:
                print("Password did NOT match!")
                return render(request, "login.html", {"error": "Invalid email or password"})
                 
        else:
            print("Password did NOT match!")
            return render(request, "login.html", {"error": "Invalid email or password"})

    return render(request, "login.html")


def search_doctors(request):
         return render(request, 'search.html')



def patient_dashboard(request):
    patient_id = request.session.get('patient_id')  # Get user ID from session
    
    if not patient_id:
        return redirect("login")  # Redirect to login if session is empty
    
    try:
        patient = patientRegister.objects.get(id=patient_id)  # Fetch patient data
        print("Patient Found:", patient.name)  # Debugging
    except patientRegister.DoesNotExist:
        return redirect("login")
    
    appointment_data_list = appointment.objects.filter(patient_id=patient).select_related('doctor_id')
    return render(request, "patient-dashboard.html",{"patient": patient,"appointment_data_list":appointment_data_list})

def doctor_dashboard(request):
    doctor_id = request.session.get('doctor_id')  # Get logged-in doctor ID

    if not doctor_id:
        return redirect("login")  # Redirect to login if not logged in
    try:
        doctor = doctorRegister.objects.get(id=doctor_id)  # Fetch the doctor
    except doctorRegister.DoesNotExist:
        return redirect("login")  # Redirect if doctor not found
    
    today = timezone.now().date()
    today_patients = appointment.objects.filter(
        doctor_id=doctor, appointment_date=today
    ).select_related('patient_id')

    upcoming_patients = appointment.objects.filter(
        doctor_id=doctor, appointment_date__gt=today
    ).select_related('patient_id')
    # upcoming_patients = appointment.objects.filter(doctor_id=doctor).select_related('patient_id')
    return render(request, "doctor-dashboard.html", {"doctor": doctor,"upcoming_patients":upcoming_patients, "today_patients": today_patients,})



def doctor_register(request):
    if request.method == "POST":
        form = doctorForm(request.POST, request.FILES)
        form = doctorForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.password = make_password(doctor.password)  # 🔒 Hash the password before saving
            doctor.save()
            return redirect('login')
            # doctor = form.save(commit=False)
            # doctor.password = make_password(doctor.password)  #  Hash the password before saving
            # doctor.save()
            # return redirect('login')
    else:
        form = doctorForm()
    return render(request, 'doctor-register.html', {'form': form})
   

def patient_register(request):
    if request.method == "POST":
        form = patientForm(request.POST, request.FILES)
        form = patientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.password = make_password(patient.password)  # 🔒 Hash the password before saving
            patient.save()
            return redirect('login')
    else:
        form = patientForm()
    return render(request, 'patient-register.html', {'form': form})

    



def terms_condition(request):
         return render(request, 'terms_condition.html')
def index(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('login')



def coming_soon(request):
    return render(request, 'coming-soon.html')
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        # Save email to database or send a confirmation
        return JsonResponse({'message': 'Subscribed successfully!'})  # Or redirect somewhere

    return render(request, 'subscribe.html')

def patient_profile(request):
    return render(request, 'patient-profile.html')


def doctor_list(request):
    doctors = doctorRegister.objects.all()  # Fetch all doctors
    return render(request, "doctor-list.html",{"doctors": doctors})


def doctor_profile(request):
    return render(request, 'doctor-profile.html')

def doctor_profile_settings(request):
    doctor_id = request.session.get('doctor_id')  # Get logged-in doctor ID

    if not doctor_id:
        return redirect("login")  # Redirect to login if not logged in
    try:
        doctor = doctorRegister.objects.get(id=doctor_id)  # Fetch the doctor
    except doctorRegister.DoesNotExist:
        return redirect("login")  # Redirect if doctor not found

    return render(request, "doctor-profile-settings.html", {"doctor": doctor})

    # return render(request, 'doctor-profile-settings.html')


from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from datetime import datetime, date, time, timedelta
from .models import  doctorRegister, patientRegister,appointment
from .forms import appointmentForm

# def book_appointment(request, doctor_id, appointment_id=None):
#     doctor = get_object_or_404(doctorRegister, id=doctor_id)
#     patient_id = request.session.get('patient_id')

#     if not patient_id:
#         return redirect('/login/')  

#     patient = get_object_or_404(patientRegister, id=patient_id)

#     # Initialize appointment object
#     appointment_obj = None
#     if appointment_id:
#         print(f"Received appointment_id: {appointment_id}")
#         appointment_obj = get_object_or_404(appointment, id=appointment_id, patient_id=patient, doctor_id=doctor)

#     if request.method == "POST":
#         print("Form submitted:", request.POST)  # Debugging
#         form = appointmentForm(request.POST, instance=appointment_obj)

#         if form.is_valid():
#             appointment_obj = form.save(commit=False)
#             appointment_obj.patient_id = patient
#             appointment_obj.doctor_id = doctor
#             appointment_obj.booking_date = now().date()

#             # appointment_obj.full_clean()  #  Correct usage on instance
#             appointment_obj.save()

#             print(f"After saving: appointment_obj ID: {appointment_obj.id}")  
#             return redirect("payment", appointment_id=appointment_obj.id, doctor_id=doctor.id)

#         print("Form errors:", form.errors)  # Debugging

#     else:
#         print(f"Prefilling form with: {appointment_obj}")  # Check if an object is actually being used

#         form = appointmentForm(instance=appointment_obj)  # Prefill form if editing

#     # Generate available time slots (9 AM to 5 PM, every 30 minutes)
#     start_time = time(9, 0)
#     end_time = time(17, 0)
#     time_slots = []
    
#     current_time = datetime.combine(date.today(), start_time)
#     while current_time.time() < end_time:
#         time_slots.append(current_time.strftime("%I:%M %p"))  # Format in 12-hour format with AM/PM
#         current_time += timedelta(minutes=30)

#     return render(request, 'booking.html', {
#         "doctor": doctor, 
#         "patient": patient,
#         "form": form,
#         "time_slots": time_slots,
#         "appointment_data_list": appointment_obj
#     })

def book_appointment(request, doctor_id, appointment_id=None):
    doctor = get_object_or_404(doctorRegister, id=doctor_id)
    patient_id = request.session.get('patient_id')

    if not patient_id:
        return redirect('/login/')  

    patient = get_object_or_404(patientRegister, id=patient_id)
    print(f"Received appointment_id: {appointment_id}")

    # Fetch existing appointment if editing
    appointment_obj = None
    if appointment_id:
        appointment_obj = get_object_or_404(appointment, id=appointment_id, patient_id=patient, doctor_id=doctor)
        print(f"Editing Existing Appointment: {appointment_obj.id}")  #  Debugging


    if request.method == "POST":
        print("Form submitted:", request.POST)  
        form = appointmentForm(request.POST, instance=appointment_obj)  #  Ensure form updates existing instance

        if form.is_valid():
            appointment_obj = form.save(commit=False)
            appointment_obj.patient_id = patient
            appointment_obj.doctor_id = doctor
            appointment_obj.booking_date = now().date()  # Update booking date
            
            appointment_obj.save()  #  Update appointment instead of creating a new one
            print(f"Appointment updated: {appointment_obj.id}")

            return redirect("payment", appointment_id=appointment_obj.id, doctor_id=doctor.id)
        else:
            print("Form errors:", form.errors)  # Debugging error messages

    else:
        form = appointmentForm(request.POST,instance=appointment_obj)  # Prefill form if editing

    # Generate available time slots (9 AM to 5 PM, every 30 minutes)
    start_time = time(9, 0)
    end_time = time(17, 0)
    time_slots = []
    
    current_time = datetime.combine(date.today(), start_time)
    while current_time.time() < end_time:
        time_slots.append(current_time.strftime("%I:%M %p"))  # Format in 12-hour format with AM/PM
        current_time += timedelta(minutes=30)

    return render(request, 'booking.html', {
        "doctor": doctor, 
        "patient": patient,
        "form": form,
        "time_slots": time_slots,
        "appointment_data_list": appointment_obj
    })


def payment_page(request, appointment_id, doctor_id):
    # Get appointment and doctor objects or return 404
    appointment_obj = get_object_or_404(appointment, id=appointment_id)
    doctor_obj = get_object_or_404(doctorRegister, id=doctor_id)

    # Convert doctor's fee to float, handling None values
    # doctor_fee = float(doctor_obj.fee) if doctor_obj.fee is not None else 0.0
    try:
        doctor_fee = float(doctor_obj.fee)  # Convert to float
    except ValueError:
        doctor_fee = 0.0  # Default to 0 if conversion fails
    GST = 0.18
    tax_amount = doctor_fee * GST
    total_amount = doctor_fee + tax_amount

    # Get or create a payment object
    payment_obj, created = Payment.objects.get_or_create(
        appointment_id=appointment_obj,  # Use the correct model field name
        doctor_id=doctor_obj,
        patient_id=appointment_obj.patient_id,  # Assuming a ForeignKey relationship
        defaults={
            'amount': total_amount,
            'payment_status': 'PENDING',
            'payment_method': '',
            'payment_date': now()
        }
    )

    if request.method == "POST":
        payment_method = request.POST.get("payment_method", "")

        # if payment_method:
        #     payment_obj.payment_method = payment_method
        #     payment_obj.payment_status = "COMPLETED"
        #     payment_obj.save()
        valid_methods = dict(Payment.METHOD_CHOICES).keys()
        if payment_method in valid_methods:
            payment_obj.payment_method = payment_method
            payment_obj.payment_status = "COMPLETED"
            payment_obj.save()

            return redirect("payment_details", appointment_id, doctor_id)

    return render(
        request,
        "payment.html",
        {
            "appointment": appointment_obj,  # Updated variable name
            "doctor": doctor_obj,
            "doctor_fee": doctor_fee,
            "tax_amount": tax_amount,
            "total_amount": total_amount,
            "payment_obj": payment_obj
        }
    )



    

def payment_details(request,appointment_id , doctor_id):
    appointment_obj = get_object_or_404(appointment, id=appointment_id)
    doctor = get_object_or_404(doctorRegister, id=doctor_id)
    payment = Payment.objects.filter(appointment_id=appointment_obj, doctor_id=doctor).first()

    if not payment:
        return HttpResponse("Payment record not found", status=404)

    return render(request, "payment-details.html", {
        "appointment": appointment_obj,
        "doctor": doctor,
        "payment": payment})


# def doctor_change_password(request):
#     doctor_id = request.session.get('doctor_id')  # Get logged-in doctor ID

#     if not doctor_id:
#         return redirect("login")  # Redirect to login if not logged in
#     try:
#         doctor = doctorRegister.objects.get(id=doctor_id)  # Fetch the doctor
#     except doctorRegister.DoesNotExist:
#         return redirect("login")  # Redirect if doctor not found

#     return render(request, "doctor-change-password.html", {"doctor": doctor})

    # return render(request, 'doctor-change-password.html')
def doctor_change_password(request):
    doctor_id = request.session.get('doctor_id')  # Get logged-in doctor ID
    if not doctor_id:
        return redirect("login")  # Redirect to login if not logged in
    
    
    try:
        doctor = doctorRegister.objects.get(id=doctor_id)
        doctor = doctorRegister.objects.get(id=doctor_id)
    except doctorRegister.DoesNotExist:
        return redirect("login")  # Redirect if doctor not found

    if request.method == 'POST':
        form = passwordChangeForm(request.POST, user=doctor)
        if form.is_valid():
            doctor.password = make_password(form.cleaned_data["new_password"])  # Hash new password
            doctor.save()
            print("Doctor ID:", doctor_id)
            print("New Password:", form.cleaned_data.get("new_password"))
    
            return redirect("doctor_dashboard")      
            
            # messages.error(request, "Error updating password. Please try again.")
    else:
        form = passwordChangeForm(user=doctor)

    return render(request, "doctor-change-password.html", {"doctor": doctor ,"form": form})




def patient_change_password(request):
    patient_id = request.session.get('patient_id')  # Get logged-in patient ID
    patient_id = request.session.get('patient_id')  # Get logged-in patient ID
    if not patient_id:
        return redirect("login")  # Redirect if not logged in
        return redirect("login")  # Redirect if not logged in
    
    try:
        patient = patientRegister.objects.get(id=patient_id)
        patient = patientRegister.objects.get(id=patient_id)
    except patientRegister.DoesNotExist:
        return redirect("login")  # Redirect if patient not found

    if request.method == 'POST':
        form = passwordChangeForm(request.POST, user=patient)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            patient.password = make_password(new_password)  # Hash new password
            patient.save()
            
            messages.success(request, "Password changed successfully.")
            return redirect("patient_dashboard")  # Redirect after successful change
        else:
            messages.error(request, "Error updating password. Please try again.")
    else:
        form = passwordChangeForm(user=patient)

    return render(request, "patient-change-password.html",{"patient":patient,"form":form})

    # return redirect("login")  # Redirect if patient not found

    # if request.method == 'POST':
    #     form = passwordChangeForm(request.POST, user=patient)
    #     if form.is_valid():
    #         new_password = form.cleaned_data['new_password']
    #         patient.password = make_password(new_password)  # Hash new password
    #         patient.save()
            
    #         messages.success(request, "Password changed successfully.")
    #         return redirect("patient_dashboard")  # Redirect after successful change
    #     else:
    #         messages.error(request, "Error updating password. Please try again.")
    # else:
    #     form = passwordChangeForm(user=patient)

    # return render(request, "patient-change-password.html",{"patient":patient,"form":form})


def password_change_successful(request):
    return render(request, 'password-change-successful.html')

def verify(request):
    return render(request, 'verify.html')

def patient_profile_settings(request):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')
    ]
    patient_id = request.session.get('patient_id')  # Get user ID from session
    
    if not patient_id:
        return redirect("login")  # Redirect to login if session is empty
    
    try:
        patient = patientRegister.objects.get(id=patient_id)  # Fetch patient data
        print("Patient Found:", patient.name)  # Debugging
    except patientRegister.DoesNotExist:
        return redirect("login")
    return render(request, 'patient-profile-settings.html', {"patient": patient})
      
def search(request):
    all_doctor=doctorRegister.objects.all
    return render(request, 'search.html',{'doctors':all_doctor})

###############################################to update doctor
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import doctorRegister,patientRegister
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token

# @csrf_exempt
# def update_doctor(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body.decode('utf-8'))  # Ensure JSON decoding

#             # Use session ID as a fallback
#             doctor_id = data.get("doctor_id", request.session.get('doctor_id'))
#             if not doctor_id:
#                 return JsonResponse({"status": "error", "message": "Doctor ID is required"})

#             doctor = get_object_or_404(doctorRegister, id=doctor_id)

#             # Update fields
#             
#             doctor.name = data.get("name", doctor.name)
#             doctor.email = data.get("email", doctor.email)
#             doctor.phno = data.get("phno", doctor.phno)
#             doctor.qualification = data.get("qualification", doctor.qualification)
#             doctor.specialization = data.get("specialization", doctor.specialization)
#             doctor.experience = data.get("experience", doctor.experience)
#             doctor.address = data.get("address", doctor.address)
#             doctor.city = data.get("city", doctor.city)
#             doctor.state = data.get("state", doctor.state)
#             doctor.clinic_name = data.get("clinic_name", doctor.clinic_name)
#             doctor.clinic_address = data.get("clinic_address", doctor.clinic_address)
#             doctor.gender = data.get("gender", doctor.gender)
#             doctor.mci_no = data.get("mci_no", doctor.mci_no)
#             doctor.fee = data.get("fee", doctor.fee)


#             doctor.save()  # Save changes

#             return JsonResponse({"status": "success", "message": "Doctor details updated successfully!"})
#         except json.JSONDecodeError:
#             return JsonResponse({"status": "error", "message": "Invalid JSON format"})
#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)})

#     return JsonResponse({"status": "error", "message": "Invalid request method"})

def update_doctor(request):
    if request.method == "POST":
        try:
            if request.FILES.get("photo"):
                doctor_id = request.POST.get("doctor_id")
                if not doctor_id:
                    return JsonResponse({"status": "error", "message": "patient ID is required"})

                doctor = get_object_or_404(patientRegister, id=doctor_id)

                # Save Image
                photo = request.FILES["photo"]
                photo_path = f"profile_pics/{doctor_id}_{photo.name}"
                doctor.photo = default_storage.save(photo_path, ContentFile(photo.read()))


                doctor.save()
                return JsonResponse({"status": "success", "message": "Image updated successfully!", "photo_url": doctor.photo.url})
            
            else:
                # Process JSON Data
                data = json.loads(request.body.decode('utf-8'))  

                # data = json.loads(request.body.decode('utf-8'))  # Ensure JSON decoding

            # Use session ID as fallback
                doctor_id = data.get("doctor_id", request.session.get('doctor_id'))
                if not doctor_id:
                    return JsonResponse({"status": "error", "message": "patient ID is required"})

                doctor = get_object_or_404(doctorRegister, id=doctor_id)
            # patient_id = request.POST.get("patient_id")
            # if not patient_id:
            #     return JsonResponse({"status": "error", "message": "patient ID is required"})

            # patient = get_object_or_404(patientRegister, id=patient_id)

            # Update fields
                doctor.name = data.get("name", doctor.name)
                doctor.email = data.get("email", doctor.email)
                doctor.phno = data.get("phno", doctor.phno)
                doctor.qualification = data.get("qualification", doctor.qualification)
                doctor.specialization = data.get("specialization", doctor.specialization)
                doctor.experience = data.get("experience", doctor.experience)
                doctor.address = data.get("address", doctor.address)
                doctor.city = data.get("city", doctor.city)
                doctor.state = data.get("state", doctor.state)
                doctor.clinic_name = data.get("clinic_name", doctor.clinic_name)
                doctor.clinic_address = data.get("clinic_address", doctor.clinic_address)
                doctor.gender = data.get("gender", doctor.gender)
                doctor.mci_no = data.get("mci_no", doctor.mci_no)
                doctor.fee = data.get("fee", doctor.fee)

                doctor.save()  # Save changes

            return JsonResponse({"status": "success", "message": "patient details updated successfully!"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method"})

@csrf_exempt  # Only for testing, in production use CSRF token properly
def upload_doctor_profile_image(request):
    if request.method == "POST":
        doctor_id = request.POST.get("doctor_id")
        image = request.FILES.get("photo")  # Get uploaded file

        if not doctor_id or not image:
            return JsonResponse({"status": "error", "message": "Missing patient ID or image"})

        try:
            doctor = doctorRegister.objects.get(id=doctor_id)

            # Define the path where the image will be saved
            file_path = f"profile_pic/{doctor_id}_{image.name}"  # Save in "media/profile_pic/"
            
            # Delete old profile image if it exists
            if doctor.profile_img and os.path.exists(os.path.join("media", str(doctor.profile_img))):
                os.remove(os.path.join("media", str(doctor.profile_img)))

            # Save the new image
            saved_path = default_storage.save(file_path, ContentFile(image.read()))

            # Update the database with the new image path
            doctor.profile_img = saved_path
            doctor.save()

            return JsonResponse({"status": "success", "photo_url": doctor.profile_img.url})
        
        except doctorRegister.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Patient not found"})

    return JsonResponse({"status": "error", "message": "Invalid request"})


@ensure_csrf_cookie  # Ensures CSRF token is sent as a cookie
def get_doctor(request, doctor_id):
    doctor = get_object_or_404(doctorRegister, id=doctor_id)
    photo_url = request.build_absolute_uri(settings.MEDIA_URL + doctor.photo.name) if doctor.photo else None
    return JsonResponse({
        "id": doctor.id,
        "name": doctor.name,
        "email": doctor.email,
        "phno": doctor.phno,
        "qualification":doctor.qualification,
        "specialization": doctor.specialization,
        "experience": doctor.experience,
        "address": doctor.address,
        "city": doctor.city,
        "state": doctor.state,
        "clinic_name": doctor.clinic_name,
        "clinic_address": doctor.clinic_address,
        "gender": doctor.gender,
        "mci_no": doctor.mci_no,
        "fee": doctor.fee,
        "photo": photo_url,  
        "csrfToken": get_token(request)  # Send CSRF token in response
    })


####################################update patient
@csrf_exempt
# def update_patient(request):
#     if request.method == "POST":
#         try:
#             if request.FILES.get("photo"):
#                 patient_id = request.POST.get("patient_id")
#                 if not patient_id:
#                     return JsonResponse({"status": "error", "message": "patient ID is required"})

#                 patient = get_object_or_404(patientRegister, id=patient_id)

#                 # Save Image
#                 photo = request.FILES["photo"]
#                 photo_path = f"profile_pics/{patient_id}_{photo.name}"
#                 patient.photo = default_storage.save(photo_path, ContentFile(photo.read()))


#                 patient.save()
#                 return JsonResponse({"status": "success", "message": "Image updated successfully!", "photo_url": patient.photo.url})
            
#             else:
#                 # Process JSON Data
#                 data = json.loads(request.body.decode('utf-8'))  

#                 # data = json.loads(request.body.decode('utf-8'))  # Ensure JSON decoding

#             # Use session ID as fallback
#                 patient_id = data.get("patient_id", request.session.get('patient_id'))
#                 if not patient_id:
#                     return JsonResponse({"status": "error", "message": "patient ID is required"})

#                 patient = get_object_or_404(patientRegister, id=patient_id)
#             # patient_id = request.POST.get("patient_id")
#             # if not patient_id:
#             #     return JsonResponse({"status": "error", "message": "patient ID is required"})

#             # patient = get_object_or_404(patientRegister, id=patient_id)

#             # Update fields
#                 patient.name = data.get("name", patient.name)
#                 patient.email = data.get("email", patient.email)
#                 patient.phno = data.get("phno", patient.phno)
#                 patient.password=data.get("password",patient.password)
#                 patient.address = data.get("address", patient.address)
#                 patient.city = data.get("city", patient.city)
#                 patient.state = data.get("state", patient.state)
#                 patient.blood_group = data.get("blood_group", patient.blood_group)
#                 patient.age = data.get("age", patient.age)
#                 patient.height = data.get("height", patient.height)
#                 patient.weight = data.get("weight", patient.weight)
#                 patient.dob = data.get("dob", patient.dob)
#                 patient.save()  # Save changes

#             return JsonResponse({"status": "success", "message": "patient details updated successfully!"})
#         except json.JSONDecodeError:
#             return JsonResponse({"status": "error", "message": "Invalid JSON format"})
#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)})

#     return JsonResponse({"status": "error", "message": "Invalid request method"})


@csrf_exempt
def update_patient(request):
    if request.method == "POST":
        try:
            patient_id = request.POST.get("patient_id")
            if not patient_id:
                return JsonResponse({"status": "error", "message": "Patient ID is required"})

            patient = get_object_or_404(patientRegister, id=patient_id)

            # Update fields
            patient.name = request.POST.get("name", patient.name)
            patient.email = request.POST.get("email", patient.email)
            patient.phno = request.POST.get("phno", patient.phno)
            patient.address = request.POST.get("address", patient.address)
            patient.city = request.POST.get("city", patient.city)
            patient.state = request.POST.get("state", patient.state)
            patient.blood_group = request.POST.get("blood_group", patient.blood_group)
            patient.age = request.POST.get("age", patient.age)
            patient.height = request.POST.get("height", patient.height)
            patient.weight = request.POST.get("weight", patient.weight)
            patient.dob = request.POST.get("dob", patient.dob)

            # Handle profile image
            if 'photo' in request.FILES:
                # Delete old profile image if it exists
                if patient.photo and os.path.exists(patient.photo.path):
                    os.remove(patient.photo.path)

                # Save new profile image
                photo = request.FILES['photo']
                photo_path = f"profile_pic/{patient_id}_{photo.name}"
                patient.photo = default_storage.save(photo_path, ContentFile(photo.read()))

            patient.save()  # Save changes

            return JsonResponse({"status": "success", "message": "Patient details updated successfully!", "photo_url": patient.photo.url if patient.photo else None})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method"})


@csrf_exempt  # Only for testing, in production use CSRF token properly
def upload_patient_profile_image(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient_id")
        image = request.FILES.get("photo")  # Get uploaded file

        if not patient_id or not image:
            return JsonResponse({"status": "error", "message": "Missing patient ID or image"})

        try:
            patient = patientRegister.objects.get(id=patient_id)

            # Define the path where the image will be saved
            file_path = f"profile_pic/{patient_id}_{image.name}"  # Save in "media/profile_pic/"
            
            # Delete old profile image if it exists
            if patient.profile_img and os.path.exists(os.path.join("media", str(patient.profile_img))):
                os.remove(os.path.join("media", str(patient.profile_img)))

            # Save the new image
            saved_path = default_storage.save(file_path, ContentFile(image.read()))

            # Update the database with the new image path
            patient.profile_img = saved_path
            patient.save()

            return JsonResponse({"status": "success", "photo_url": patient.profile_img.url})
        
        except patientRegister.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Patient not found"})

    return JsonResponse({"status": "error", "message": "Invalid request"})


@ensure_csrf_cookie  # Ensures CSRF token is sent as a cookie  
def get_patient(request, patient_id):
    patient = get_object_or_404(patientRegister, id=patient_id)

    # Construct the full photo URL if the patient has an image
    photo_url = request.build_absolute_uri(settings.MEDIA_URL + patient.photo.name) if patient.photo else None
    return JsonResponse({
        "id": patient.id,
        "name": patient.name,
        "email": patient.email,
        "phno": patient.phno,
        "password":patient.password,
        "address": patient.address,
        "city": patient.city,
        "state": patient.state,
        "blood_group": patient.blood_group,
        "age": patient.age,
        "height": patient.height,
        "weight": patient.weight,
        "dob": patient.dob,
        "photo": photo_url,  
        "csrfToken": get_token(request)  # Send CSRF token in response
    })




def admin_profile_settings(request):
    return render(request, 'admin-profile-settings.html')


def admin_change_password(request):
    return render(request, 'admin-change-password.html')

def admin_manage_docters(request):
    all_doctor=doctorRegister.objects.all
    return render(request, 'admin_manage_docters.html',{'all':all_doctor})

def admin_manage_patients(request):
        all_patient=patientRegister.objects.all
        return render(request, 'admin_manage_patients.html',{'all':all_patient})

def admin_manage_appointments(request):
    all_appointments=appointment.objects.all
    return render(request ,'admin_manage_appointments.html',{'all':all_appointments})

def admin_logout(request):
    request.session.flush()  # Clears all session data (logs out admin)
    return redirect('/') 
 # Redirects to home page after logout 
def admin_change_password(request):
    admin_id = request.session.get('admin_id')  # Get logged-in admin ID
    if not admin_id:
        return redirect("admin_login")  # Redirect to admin login if not logged in
    
    try:
        admin = adminLogin.objects.get(id=admin_id)
    except adminLogin.DoesNotExist:
        return redirect("admin_login")  # Redirect if admin not found

    if request.method == 'POST':
        form = passwordChangeForm(request.POST, user=admin)
        if form.is_valid():
            admin.password = make_password(form.cleaned_data["new_password"])  # Hash new password
            admin.save()
            print("Admin ID:", admin_id)
            print("New Password:", form.cleaned_data.get("new_password"))
    
            return redirect("admin_dashboard")  # Redirect to admin dashboard
            
            # messages.error(request, "Error updating password. Please try again.")
    else:
        form = passwordChangeForm(user=admin)

    return render(request, "admin-change-password.html", {"admin": admin, "form": form})




def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            admin = adminLogin.objects.get(email=email)

            # Check if the entered password matches the stored hashed password
            if check_password(password, admin.password):
                request.session['admin_id'] = admin.id  # Store admin session
                return redirect('admin_dashboard')  # Ensure this matches your routes
            else:
                messages.error(request, "Invalid password.")
        
        except adminLogin.DoesNotExist:
            messages.error(request,"Invalid email or username.")  

    return render(request, 'admin_login.html')  # Return the login page with error messages if any


from django.core.mail import send_mail, BadHeaderError

# def is_admin_logged_in(request):
#     return 'admin_id' in request.session

def admin_dashboard(request):
        if 'admin_id' not in request.session:
                return redirect('admin_login')  # Redirect if not logged in

        # Get all unapproved doctors
        pending_doctors = doctorRegister.objects.filter(is_approved=False)
        approved_doctors = doctorRegister.objects.filter(is_approved=True)
        return render(request, 'admin-dashboard.html',{'pending_doctors': pending_doctors, 'approved_doctors': approved_doctors})

def approve_doctor(request, doctor_id):
    doctor = get_object_or_404(doctorRegister, id=doctor_id)
    doctor.is_approved = True
    doctor.save()

    subject = 'Your Account Has Been Approved!'
    message = f'Hello {doctor.name}, your account has been approved. You can now log in.'
    recipient_email = doctor.email


    try:
        send_mail(
            subject,
            message,
            'webdoctors123@gmail.com',  # Ensure this matches EMAIL_HOST_USER
            [recipient_email],
            fail_silently=False,
        )
        print(" Email sent successfully!")  # Debugging log
    except BadHeaderError:
        print(" Invalid email header!")
    except Exception as e:
        print(f" Email failed: {e}")

    messages.success(request, f"Doctor {doctor.name} has been approved successfully.")
    return redirect('admin_dashboard')


def reject_doctor(request, doctor_id):
    # if not is_admin_logged_in(request):
    #     return redirect('admin_login')

    doctor = get_object_or_404(doctorRegister, id=doctor_id)
    doctor.is_approved = False
    doctor.save()
    # doctor.delete()

    messages.error(request, f"Doctor {doctor.name} has been rejected and removed.")
    return redirect('admin_dashboard')
