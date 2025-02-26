# import datetime
from datetime import time, timedelta
import datetime
from pyexpat.errors import messages  # Correct way to use strptime
from django.urls import reverse
from datetime import datetime, timedelta, time, date
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from .forms import patientForm,doctorForm ,appointmentForm

# from .forms import doctorForm
from .models import patientRegister,doctorRegister
from .models import appointment

# Create your views here.
# from django.shortcuts import render

from django.shortcuts import get_object_or_404


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

def login(request):
    email = None
    password = None
    user_type = None
    user = None

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")
        # patient=patientRegister.objects.get(email=email,password=password)

        # doctor = doctorRegister.objects.get(email=email, password=password)  
        user = None

        if user_type == "patient":
            try:
                user = patientRegister.objects.get(email=email)
                request.session['patient_id'] = user.id
            except patientRegister.DoesNotExist:
                return render(request, "login.html", {"error": "Patient does not exist"})

        elif user_type == "doctor":
            try:
                user = doctorRegister.objects.get(email=email)
                request.session['doctor_id'] = user.id  # Store doctor ID in session
            except doctorRegister.DoesNotExist:
                return render(request, "login.html", {"error": "Doctor does not exist"})

        else:
            return render(request, "login.html", {"error": "Invalid user type"})

        # ✅ **Manually check the password**
        if password == user.password:
            # Redirect based on user type
            if user_type == "patient":
                return redirect("patient_dashboard")  # Update with actual patient dashboard URL
            elif user_type == "doctor":
                return redirect("doctor_dashboard")  # Update with actual doctor dashboard URL

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
    return render(request, "patient-dashboard.html",{"patient": patient})

def doctor_dashboard(request):
    doctor_id = request.session.get('doctor_id')  # Get logged-in doctor ID

    if not doctor_id:
        return redirect("login")  # Redirect to login if not logged in
    try:
        doctor = doctorRegister.objects.get(id=doctor_id)  # Fetch the doctor
    except doctorRegister.DoesNotExist:
        return redirect("login")  # Redirect if doctor not found

    return render(request, "doctor-dashboard.html", {"doctor": doctor})

def admin_dashboard(request):
         return render(request, 'admin-dashboard.html')


def doctor_register(request):
    if request.method == "POST":
        form = doctorForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            print("Form is valid, saving the data.")  # Debug print
            form.save()
            return redirect('login')  # Redirect instead of rendering login page directly
        else:
            print("Form errors:", form.errors)  # Debug print
    else:
        form = doctorForm()  # Create an empty form for GET request

    return render(request, 'doctor-register.html', {'form': form})  # Pass form to template


def patient_register(request):

    if request.method == "POST":
        form = patientForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect instead of rendering login page directly
        else:
            print("Form errors:", form.errors)  # Debug print
            
    else:
        form = patientForm()  # Create an empty form for GET request

    return render(request, 'patient-register.html', {'form': form})  # Pass form to template

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


def book_appointment(request, doctor_id):
    patient_id = request.session.get('patient_id')  # Get patient ID from session
    if not patient_id:
        return redirect('/login/')  # Redirect to login if not logged in

    patient = get_object_or_404(patientRegister, id=patient_id)  
    doctor = get_object_or_404(doctorRegister, id=doctor_id)

    # Generate available time slots (9 AM to 5 PM, every 30 minutes)
    start_time = time(9, 0)
    end_time = time(17, 0)
    time_slots = []
    
    current_time = datetime.combine(date.today(), start_time)
    while current_time.time() < end_time:
        time_slots.append(current_time.strftime("%I:%M %p"))  # Format in 12-hour format with AM/PM
        current_time += timedelta(minutes=30)

    if request.method == "POST":
        print("Form submitted:", request.POST)  # Debugging: Print submitted data
        form = appointmentForm(request.POST)
        
        if form.is_valid():
            appointment_obj = form.save(commit=False)
            appointment_obj.patient_id = patient
            appointment_obj.doctor_id = doctor
            appointment_obj.save() 
            
            print("Appointment saved:", appointment_obj)  # Debugging: Print saved appointment
            return redirect("payment", appointment_id=appointment_obj.id, doctor_id=doctor.id)

        
        print("Form errors:", form.errors)  # Debugging: Print form errors

    else:
        form = appointmentForm()
    
    return render(request, 'booking.html', {
        "doctor": doctor, 
        "patient": patient,
        "form": form,
        "time_slots": time_slots
    })




def payment(request, appointment_id , doctor_id):
    # Try to get the appointment, or return a 404 page if not found
    
    Appointment = get_object_or_404(appointment,id=appointment_id)
    doctor=get_object_or_404(doctorRegister,id=doctor_id)
    doctor_fee = doctor.fee 
    GST = 0.18
    tax_amount = doctor_fee * GST
    total_amount = doctor_fee + tax_amount
    return render(request, "payment.html", {"Appointment": Appointment,"doctor":doctor,"doctor_fee": doctor_fee,
        "tax_amount": tax_amount,
        "total_amount": total_amount})


def doctor_change_password(request):
    doctor_id = request.session.get('doctor_id')  # Get logged-in doctor ID

    if not doctor_id:
        return redirect("login")  # Redirect to login if not logged in
    try:
        doctor = doctorRegister.objects.get(id=doctor_id)  # Fetch the doctor
    except doctorRegister.DoesNotExist:
        return redirect("login")  # Redirect if doctor not found

    return render(request, "doctor-change-password.html", {"doctor": doctor})

    # return render(request, 'doctor-change-password.html')

def patient_change_password(request):
    patient_id = request.session.get('patient_id')  # Get user ID from session
    
    if not patient_id:
        return redirect("login")  # Redirect to login if session is empty
    
    try:
        patient = patientRegister.objects.get(id=patient_id)  # Fetch patient data
        print("Patient Found:", patient.name)  # Debugging
    except patientRegister.DoesNotExist:
        return redirect("login")
    return render(request, 'patient-change-password.html',{"patient": patient})

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