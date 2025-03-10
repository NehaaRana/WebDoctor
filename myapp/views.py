# import datetime
from datetime import time, timedelta
import datetime
from http import client
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
from django.contrib.auth.decorators import login_required
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
from .models import appointment,Payment,review
import os

# import razorpay
from webDoctor.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRETE_KEY
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

# def about_us(request):
#     return render(request, 'about-us.html')

def about_us(request):
    print("🚀 about_us view is being executed!")

    profile = None
    user_type = None

    # Check session data
    patient_id = request.session.get("patient_id")
    doctor_id = request.session.get("doctor_id")

    print("🔍 Patient ID from session:", patient_id)
    print("🔍 Doctor ID from session:", doctor_id)

    try:
        if patient_id:
            profile = patientRegister.objects.get(id=patient_id)
            user_type = "patient"
        elif doctor_id:
            profile = doctorRegister.objects.get(id=doctor_id)
            user_type = "doctor"

        if profile:
            print("✅ Profile Found:", profile.name)
    except Exception as e:
        print("❌ Error fetching user profile:", e)

    return render(request, "about-us.html", {"profile": profile, "user_type": user_type})






def about(request):
    return render(request, 'about.html')

def contact(request):
         return render(request, 'contact.html')

# def contact_us(request):
#          return render(request, 'contact-us.html')

def contact_us(request):
    print("🚀 contact_us view is being executed!")

    profile = None
    user_type = None

    # Retrieve session data
    patient_id = request.session.get("patient_id")
    doctor_id = request.session.get("doctor_id")

    print("🔍 Patient ID from session:", patient_id)
    print("🔍 Doctor ID from session:", doctor_id)

    try:
        if patient_id:
            profile = patientRegister.objects.get(id=patient_id)
            user_type = "patient"
        elif doctor_id:
            profile = doctorRegister.objects.get(id=doctor_id)
            user_type = "doctor"

        if profile:
            print("✅ Profile Found:", profile.name)
    except Exception as e:
        print("❌ Error fetching user profile:", e)

    return render(request, "contact-us.html", {"profile": profile, "user_type": user_type})


def register(request):
         return render(request, 'register.html')



def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")
        user = None

        print(f"Login attempt: Email={email}, UserType={user_type}")

        if user_type == "patient":
            try:
                user = patientRegister.objects.get(email=email)
                request.session['patient_id'] = user.id
                print(f"Patient found: {user.email}")
            except patientRegister.DoesNotExist:
                messages.error(request, "Patient does not exist!")
                return redirect("login")  # Redirect instead of render to persist messages

        elif user_type == "doctor":
            try:
                user = doctorRegister.objects.get(email=email)

                if not user.is_approved:
                    messages.warning(request, "Your account is pending approval. Please wait for admin approval.")
                    return redirect("login")

                request.session['doctor_id'] = user.id
                print(f"Doctor found: {user.email}")

            except doctorRegister.DoesNotExist:
                messages.error(request, "Doctor does not exist!")
                return redirect("login")

        else:
            messages.error(request, "Invalid user type!")
            return redirect("login")

        # **Check password securely**
        if check_password(password, user.password):
            messages.success(request, "Login successful! Redirecting...")
            if user_type == "patient":
                return redirect("patient_dashboard")
            elif user_type == "doctor":
                return redirect("doctor_dashboard")
        else:
            messages.error(request, "Invalid email or password!")
            return redirect("login")

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


# def doctor_register(request):
#     if request.method == "POST":
#         form = doctorForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             doctor = form.save(commit=False)
#             doctor.password = make_password(doctor.password)  # Hash the password
            
#             if doctor.fee is None:  
#                 doctor.fee = 0  # Ensure fee is not None
            
#             doctor.save()
#             messages.success(request, "Registration successful! Please log in.")  # Success message
#             return redirect('login')
#         else:
#             messages.error(request, "Registration failed! Please correct the errors below.")  # Error message

#     else:
#         form = doctorForm()

#     return render(request, 'doctor-register.html', {'form': form})
   




# def patient_register(request):
#     if request.method == "POST":
#         form = patientForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             patient = form.save(commit=False)
#             patient.password = make_password(patient.password)  # Hash password before saving
#             patient.save()
            
#             messages.success(request, "Registration successful! Please log in.")  # Success alert
#             return redirect('login')
#         else:
#             messages.error(request, "Registration failed! Please check your details.")  # Error alert

#     else:
#         form = patientForm()

#     return render(request, 'patient-register.html', {'form': form})
    



def terms_condition(request):
         return render(request, 'terms_condition.html')
def index(request):
    print("🚀 about_us view is being executed!")

    profile = None
    user_type = None

    # Check session data
    patient_id = request.session.get("patient_id")
    doctor_id = request.session.get("doctor_id")

    print("🔍 Patient ID from session:", patient_id)
    print("🔍 Doctor ID from session:", doctor_id)

    try:
        if patient_id:
            profile = patientRegister.objects.get(id=patient_id)
            user_type = "patient"
        elif doctor_id:
            profile = doctorRegister.objects.get(id=doctor_id)
            user_type = "doctor"

        if profile:
            print("✅ Profile Found:", profile.name)
    except Exception as e:
        print("❌ Error fetching user profile:", e)

    return render(request, "index.html", {"profile": profile, "user_type": user_type})

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


# def doctor_list(request):
#     doctors = doctorRegister.objects.all()  # Fetch all doctors
#     print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")
#     return render(request, "doctor-list.html",{"doctors": doctors})

def doctor_list(request):
    doctors = doctorRegister.objects.all()  # Fetch all doctors
    user_type = None
    profile = None

    # Check if a patient is logged in
    if request.session.get('patient_id'):
        try:
            profile = patientRegister.objects.get(id=request.session['patient_id'])
            user_type = "patient"
        except patientRegister.DoesNotExist:
            request.session.flush()  # Clear session if user not found

    # Check if a doctor is logged in
    elif request.session.get('doctor_id'):
        try:
            profile = doctorRegister.objects.get(id=request.session['doctor_id'])
            user_type = "doctor"
        except doctorRegister.DoesNotExist:
            request.session.flush()  # Clear session if user not found

    return render(request, "doctor-list.html", {
        "doctors": doctors,
        "profile": profile,
        "user_type": user_type  # Pass user type for navbar logic
    })


# def doctor_profile(request, doctor_id):
#     doctor = get_object_or_404(doctorRegister, id=doctor_id)  # Fetch doctor by ID
#     reviews = review.objects.filter(doctor_id=doctor.id)

#     # Check if the logged-in user is a doctor or patient
#      # Determine if the logged-in user is a doctor or patient
#     user_data = None
#     user_role = None

#     if request.user.is_authenticated:
#         # Check if the user is a doctor
#         if doctorRegister.objects.filter(user=request.user).exists():
#             user_data = doctorRegister.objects.get(user=request.user)
#             user_role = "doctor"
#         # Check if the user is a patient
#         elif patientRegister.objects.filter(user=request.user).exists():
#             user_data = patientRegister.objects.get(user=request.user)
#             user_role = "patient"
#     return render(request, 'doctor-profile.html', {'doctor': doctor,  'reviews': reviews, 'user_data': user_data,   'user_role': user_role, })

def doctor_profile(request, doctor_id):
    doctor = get_object_or_404(doctorRegister, id=doctor_id)  # Fetch doctor by ID
    reviews = review.objects.filter(doctor_id=doctor.id)

    # Initialize variables
    profile = None
    user_type = None

    # Check if a patient is logged in
    if request.session.get('patient_id'):
        try:
            profile = patientRegister.objects.get(id=request.session['patient_id'])
            user_type = "patient"
        except patientRegister.DoesNotExist:
            request.session.flush()  # Clear session if user not found

    # Check if a doctor is logged in
    elif request.session.get('doctor_id'):
        try:
            profile = doctorRegister.objects.get(id=request.session['doctor_id'])
            user_type = "doctor"
        except doctorRegister.DoesNotExist:
            request.session.flush()  # Clear session if user not found

    return render(request, 'doctor-profile.html', {
        'doctor': doctor,
        'reviews': reviews,
        'profile': profile,
        'user_type': user_type
    })

def doctor_profile_cancel_appointment(request, doctor_id):
    doctor = get_object_or_404(doctorRegister, id=doctor_id)  # Fetch doctor by ID
    return render(request, 'doctor-profile-cancel-appointment.html', {'doctor': doctor})



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

# @login_required(login_url='/login/')  # Redirects to login page if user is not logged in
def book_appointment(request, doctor_id, appointment_id=None):
    doctor = get_object_or_404(doctorRegister, id=doctor_id)
    patient_id = request.session.get('patient_id')

    if not patient_id:
         messages.error(request, "You must be logged in to book an appointment.")
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
             # **Set success message**
            messages.success(request, "Appointment booked successfully! Redirecting to payment...")
            return redirect("payment", appointment_id=appointment_obj.id, doctor_id=doctor.id)
        else:
            print("Form errors:", form.errors)  # Debugging error messages
            messages.error(request, "Failed to book appointment. Please check the form and try again.")
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


# for clear message
# from django.contrib.messages import get_messages
# from django.http import JsonResponse

# def clear_messages(request):
#     request.session.pop('toastr_message', None)
#     request.session.pop('toastr_tag', None)
#     return JsonResponse({"status": "success"})
# def clear_messages(request):
#     storage = get_messages(request)
#     list(storage)  # This clears the messages
#     return JsonResponse({"status": "success"})


#for cancel appointment

def cancel_appointment(request, appointment_id):
    appointment_obj = get_object_or_404(appointment, id=appointment_id)

    if appointment_obj.status == "Cancelled":
        messages.warning(request, "This appointment is already cancelled.")
    else:
        appointment_obj.status = "Cancelled"
        appointment_obj.save()
        messages.success(request, "Appointment has been successfully cancelled.")

    return redirect('patient_dashboard') # Redirect to doctor dashboard


#update appointment status
def update_appointment_status(request, appointment_id, status):
    appointment_obj = get_object_or_404(appointment, id=appointment_id)

    if status == "Confirm":
        appointment_obj.status = "Confirm"
        messages.success(request, "Appointment marked as Confirm.")
         # Send Confirmation Email
        subject = "Appointment Confirmed "
        message = f"Dear {appointment_obj.patient_id.name},\n\nYour appointment with Dr. {appointment_obj.doctor_id.name} on {appointment_obj.appointment_date} at {appointment_obj.appointment_time} has been confirmed.\n\nThank you!"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [appointment_obj.patient_id.email])

    elif status == "Cancelled":
        appointment_obj.status = "Cancelled"
        messages.warning(request, "Appointment has been Cancelled.")


        subject = "Appointment Cancelled"
        message = f"Dear {appointment_obj.patient_id.name},\n\nWe regret to inform you that your appointment with Dr. {appointment_obj.doctor_id.name} on {appointment_obj.appointment_date} at {appointment_obj.appointment_time} has been cancelled.\n\nPlease contact the clinic for rescheduling."
        send_mail(subject, message, settings.EMAIL_HOST_USER, [appointment_obj.patient_id.email])

    appointment_obj.save()
    return redirect('doctor_dashboard')  # Redirect to doctor's dashboard

# def payment_page(request, appointment_id, doctor_id):
#     # Get appointment and doctor objects or return 404
#     appointment_obj = get_object_or_404(appointment, id=appointment_id)
#     doctor_obj = get_object_or_404(doctorRegister, id=doctor_id)

#     # Convert doctor's fee to float, handling None values
#     # doctor_fee = float(doctor_obj.fee) if doctor_obj.fee is not None else 0.0
#     try:
#         doctor_fee = float(doctor_obj.fee)  # Convert to float
#     except ValueError:
#         doctor_fee = 0.0  # Default to 0 if conversion fails
#     GST = 0.18
#     tax_amount = doctor_fee * GST
#     total_amount = doctor_fee + tax_amount

#     # Get or create a payment object
#     payment_obj, created = Payment.objects.get_or_create(
#         appointment_id=appointment_obj,  # Use the correct model field name
#         doctor_id=doctor_obj,
#         patient_id=appointment_obj.patient_id,  # Assuming a ForeignKey relationship
#         defaults={
#             'amount': total_amount,
#             'payment_status': 'PENDING',
#             'payment_method': '',
#             'payment_date': now()
#         }
#     )

#     if request.method == "POST":
#         payment_method = request.POST.get("payment_method", "")

#         # if payment_method:
#         #     payment_obj.payment_method = payment_method
#         #     payment_obj.payment_status = "COMPLETED"
#         #     payment_obj.save()
#         valid_methods = dict(Payment.METHOD_CHOICES).keys()
#         if payment_method in valid_methods:
#             payment_obj.payment_method = payment_method
#             payment_obj.payment_status = "COMPLETED"
#             payment_obj.save()

#             return redirect("payment_details", appointment_id, doctor_id)

#     return render(
#         request,
#         "payment.html",
#         {
#             "appointment": appointment_obj,  # Updated variable name
#             "doctor": doctor_obj,
#             "doctor_fee": doctor_fee,
#             "tax_amount": tax_amount,
#             "total_amount": total_amount,
#             "payment_obj": payment_obj
#         }
#     )


from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import json
from .models import appointment,Payment
import razorpay
from django.conf import settings
from django.shortcuts import render

# Initialize Razorpay Client
client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRETE_KEY))


# def payment_page(request, appointment_id, doctor_id):
#     # Get appointment and doctor objects or return 404
#     appointment_obj = get_object_or_404(appointment, id=appointment_id)
#     doctor_obj = get_object_or_404(doctorRegister, id=doctor_id)
#     patient_obj = appointment_obj.patient_id  # Assuming ForeignKey to User/Patient model

#     # Fetch user details
#     user_name = patient_obj.name
#     user_email = patient_obj.email
#     user_phno = patient_obj.phno

#     try:
#         doctor_fee = float(doctor_obj.fee)  # Convert to float
#     except ValueError:
#         doctor_fee = 0.0  # Default to 0 if conversion fails
#     GST = 0.18  
#     tax_amount = doctor_fee * GST
#     total_amount = doctor_fee + tax_amount

#     DATA = {
#         "amount": int(total_amount * 100),  # Convert INR to paise
#         "currency": "INR",
#         "receipt": f"receipt_{appointment_id}",
#         "payment_capture": 0,  # Allow method selection
#         "notes": {
#             "doctor": doctor_obj.name,
#             "appointment_id": appointment_id
#         }
#     }

#     # Create order
#     payment_order = client.order.create(DATA)
#     payment_order_id = payment_order['id']

   

#     context = {
#         "appointment": appointment_obj,
#         "doctor": doctor_obj,
#         "doctor_fee": doctor_fee,
#         "tax_amount": tax_amount,
#         "total_amount": total_amount,
#         "api_key": RAZORPAY_API_KEY,
#         "order_id": payment_order_id,
#          "user_name": user_name,
#         "user_email": user_email,
#         "user_phno": user_phno
#     }

#     return render(request, "payment.html", context)


def payment_page(request, appointment_id, doctor_id):
    # Get appointment and doctor objects or return 404
    appointment_obj = get_object_or_404(appointment, id=appointment_id)
    doctor_obj = get_object_or_404(doctorRegister, id=doctor_id)
    patient_obj = appointment_obj.patient_id  # Assuming ForeignKey to Patient model

    # Fetch user details
    user_name = patient_obj.name
    user_email = patient_obj.email
    user_phno = patient_obj.phno

    try:
        doctor_fee = float(doctor_obj.fee)  # Convert to float
    except ValueError:
        doctor_fee = 0.0  # Default to 0 if conversion fails

    GST = 0.18  
    tax_amount = doctor_fee * GST
    total_amount = doctor_fee + tax_amount

    DATA = {
        "amount": int(total_amount * 100),  # Convert INR to paise
        "currency": "INR",
        "receipt": f"receipt_{appointment_id}",
        "payment_capture": 0,  # Allow method selection
        "notes": {
            "doctor": doctor_obj.name,
            "appointment_id": appointment_id
        }
    }

    # Create Razorpay order
    client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRETE_KEY))
    payment_order = client.order.create(DATA)
    payment_order_id = payment_order['id']

    # Determine if the logged-in user is a doctor or patient
    user_type = None
    if request.session.get('patient_id'):
        user_type = "patient"  # Patient logged in
    elif request.session.get('doctor_id'):
        user_type = "doctor"  # Doctor logged in

    context = {
        "appointment": appointment_obj,
        "doctor": doctor_obj,
        "patient": patient_obj,
        "doctor_fee": doctor_fee,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
        "api_key": RAZORPAY_API_KEY,
        "order_id": payment_order_id,
        "user_name": user_name,
        "user_email": user_email,
        "user_phno": user_phno,
        "user_type": user_type  # This helps hide the profile section for patients
    }

    return render(request, "payment.html", context)


from django.http import JsonResponse
import hmac
import hashlib
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        try:
            data = request.POST if request.POST else json.loads(request.body)

            razorpay_order_id = data.get("razorpay_order_id")
            razorpay_payment_id = data.get("razorpay_payment_id")
            razorpay_signature = data.get("razorpay_signature")
            appointment_id = data.get("appointment_id")
            amount_paid = data.get("amount")
            if amount_paid is None:
                return JsonResponse({"status": "error", "message": "Amount not provided"}, status=400)

                # Convert amount_paid to a float if needed (and adjust if it is in paise)
            amount_paid = float(amount_paid)

            if not (razorpay_order_id and razorpay_payment_id and razorpay_signature and appointment_id):
                return JsonResponse({"status": "error", "message": "Missing required parameters"}, status=400)

            # Convert appointment_id to an actual instance
            try:
                appointment_obj = appointment.objects.get(id=appointment_id)
            except appointment.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Appointment not found"}, status=404)

            # Verify Razorpay signature
            key_secret = RAZORPAY_API_SECRETE_KEY.encode()
            generated_signature = hmac.new(
                key_secret,
                f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
                hashlib.sha256
            ).hexdigest()

            if generated_signature.lower() == razorpay_signature.lower():
                # ✅ Store payment details in database
                payment_obj, created = Payment.objects.get_or_create(
                    appointment_id=appointment_obj,  # Pass actual instance, not ID
                    defaults={
                        "razorpay_order_id": razorpay_order_id,
                        "razorpay_payment_id": razorpay_payment_id,
                        "razorpay_signature": razorpay_signature,
                        "amount": amount_paid,  # Replace with actual amount
                        "payment_status": "COMPLETED",
                        "payment_method": "Razorpay",
                        "payment_date": timezone.now(),
                        "doctor_id": appointment_obj.doctor_id,  # Use instance reference
                        "patient_id": appointment_obj.patient_id  # Use instance reference
                    }
                )

                # If payment already exists, update it
                if not created:
                    payment_obj.razorpay_order_id = razorpay_order_id
                    payment_obj.razorpay_payment_id = razorpay_payment_id
                    payment_obj.razorpay_signature = razorpay_signature
                    payment_obj.payment_status = "COMPLETED"
                    payment_obj.payment_method = "Razorpay"
                    payment_obj.payment_date = timezone.now()
                    payment_obj.save()

                return JsonResponse({"status": "success", "appointment_id": appointment_id})

            return JsonResponse({"status": "failure", "message": "Signature mismatch"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

# def payment_success_page(request, appointment_id, doctor_id):
#     doctor = get_object_or_404(doctorRegister, id=doctor_id)
#     appointment_obj = get_object_or_404(appointment, id=appointment_id)

#     if request.method == "POST":
#         rating = request.POST.get("rating")
#         review_text = request.POST.get("review_text")

#         if rating and review_text:
#             review_obj = review.objects.create(
#                 patient_id=appointment_obj.patient_id,
#                 doctor_id=doctor,
#                 appointment_id=appointment_obj,
#                 rating=rating,
#                 review_text=review_text,
#                 review_date=timezone.now(),
#             )
#             return redirect(f"/doctor_profile/{doctor_id}/")  # Redirect after review submission

#     # return render(request, "reviews.html", {"doctor": doctor, "appointment": appointment_obj})

#     return render(request, "payment-success-page.html", {"doctor": doctor, "appointment": appointment_obj})  # Load success page template

def payment_success_page(request, appointment_id, doctor_id):
    doctor = get_object_or_404(doctorRegister, id=doctor_id)
    appointment_obj = get_object_or_404(appointment, id=appointment_id)

    # try:
    #     payment = Payment.objects.get(appointment=appointment_obj)
    # except Payment.DoesNotExist:
    #     payment = None

     # Fetch the payment record
    payment = Payment.objects.filter(appointment_id=appointment_id).first()


    if request.method == "POST":
        rating = request.POST.get("rating")
        review_text = request.POST.get("review_text")

        if rating and review_text:
            review_obj = review.objects.create(
                patient_id=appointment_obj.patient_id,
                doctor_id=doctor,
                appointment_id=appointment_obj,
                rating=rating,
                review_text=review_text,
                review_date=timezone.now(),
            )
            return redirect(f"/")  # Redirect after review submission

    # return render(request, "reviews.html", {"doctor": doctor, "appointment": appointment_obj})

    return render(request, "payment-success-page.html", {"doctor": doctor, "appointment": appointment_obj,"payment": payment })  # Load success page template
    

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




# def patient_change_password(request):
#     patient_id = request.session.get('patient_id')  # Get logged-in patient ID
#     patient_id = request.session.get('patient_id')  # Get logged-in patient ID
#     if not patient_id:
#         return redirect("login")  # Redirect if not logged in
       
    
#     try:
#         patient = patientRegister.objects.get(id=patient_id)
#         patient = patientRegister.objects.get(id=patient_id)
#     except patientRegister.DoesNotExist:
#         return redirect("login")  # Redirect if patient not found

#     if request.method == 'POST':
#         form = passwordChangeForm(request.POST, user=patient)
#         if form.is_valid():
#             new_password = form.cleaned_data['new_password']
#             patient.password = make_password(new_password)  # Hash new password
#             patient.save()
            
#             messages.success(request, "Password changed successfully.")
#             return redirect("patient_dashboard")  # Redirect after successful change
#         else:
#             messages.error(request, "Error updating password. Please try again.")
#     else:
#         form = passwordChangeForm(user=patient)

#     return render(request, "patient-change-password.html",{"patient":patient,"form":form})



def patient_change_password(request):
    patient_id = request.session.get('patient_id')  
    if not patient_id:
        return redirect("login")  # Redirect if not logged in
    
    try:
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

    return render(request, "patient-change-password.html", {"patient": patient, "form": form})




def password_change_successful(request):
    return render(request, 'password-change-successful.html')

def verify(request):
    return render(request, 'verify.html')

# def patient_profile_settings(request):
#     patient_id = request.session.get('patient_id')  # Get patient ID from session

#     if not patient_id:
#         messages.error(request, "You need to log in first.")  # Alert for unauthenticated users
#         return redirect("login")  # Redirect to login if not authenticated

#     try:
#         patient = patientRegister.objects.get(id=patient_id)  # Fetch patient data
#     except patientRegister.DoesNotExist:
#         messages.error(request, "Patient not found. Please log in again.")  # Alert for invalid patient
#         return redirect("login")

#     if request.method == "POST":
#         data = request.POST
#         print(" Received Data:", data)  # Debugging

#         # Check if POST data is actually being sent
#         if not data:
#             print(" No data received in POST request!")

#         # Update fields only if values are provided
#         patient.phno = data.get("phone", patient.phno)
#         patient.address = data.get("address", patient.address)
#         patient.city = data.get("city", patient.city)
#         patient.state = data.get("state", patient.state)
#         patient.blood_group = data.get("blood_group", patient.blood_group)
#         patient.age = data.get("age", patient.age)
#         patient.height = data.get("height", patient.height)
#         patient.weight = data.get("weight", patient.weight)
#         patient.dob = data.get("dob", patient.dob)

#         print(" Before Saving:", patient.__dict__)  # Debugging

#         patient.save()  # Save data to database

#         print("Data Saved Successfully!")  # Confirmation

#         messages.success(request, "Profile details added successfully!")
#         return redirect("patient_profile_settings")  # Reload page with updated details

#     return render(request, 'patient-profile-settings.html', {"patient": patient})
    


def patient_profile_settings(request):
    patient_id = request.session.get('patient_id')  # Get patient ID from session

    if not patient_id:
        messages.error(request, "You need to log in first.")  # Alert for unauthenticated users
        return redirect("login")

    try:
        patient = patientRegister.objects.get(id=patient_id)  # Fetch patient data
    except patientRegister.DoesNotExist:
        messages.error(request, "Patient not found. Please log in again.")  # Alert for invalid patient
        return redirect("login")

    if request.method == "POST":
        data = request.POST
        print("Received Data:", data)  # Debugging

        if not data:
            print("No data received in POST request!")

        # Store old values for comparison
        old_data = {
            "phno": patient.phno,
            "address": patient.address,
            "city": patient.city,
            "state": patient.state,
            "blood_group": patient.blood_group,
            "age": patient.age,
            "height": patient.height,
            "weight": patient.weight,
            "dob": patient.dob,
        }

        # Update fields only if values are provided
        patient.phno = data.get("phone", patient.phno)
        patient.address = data.get("address", patient.address)
        patient.city = data.get("city", patient.city)
        patient.state = data.get("state", patient.state)
        patient.blood_group = data.get("blood_group", patient.blood_group)
        patient.age = data.get("age", patient.age)
        patient.height = data.get("height", patient.height)
        patient.weight = data.get("weight", patient.weight)
        patient.dob = data.get("dob", patient.dob)

        # Compare new values with old values
        updated_fields = [
            field for field in old_data if getattr(patient, field) != old_data[field]
        ]

        if updated_fields:
            patient.save()  # Save data to database
            messages.success(request, " Profile updated successfully!")  # Success alert
        else:
            messages.warning(request, "No changes were made.")  # Warning alert

        return redirect("patient_profile_settings")  # Reload page with updated details

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


@csrf_exempt
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
    photo_url = request.build_absolute_uri(settings.MEDIA_URL + doctor.profile_img.name) if doctor.profile_img else None
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
def update_patient(request):
    if request.method == "POST":
        try:
            if request.FILES.get("photo"):
                patient_id = request.POST.get("patient_id")
                if not patient_id:
                    return JsonResponse({"status": "error", "message": "Patient ID is required"})

                patient = get_object_or_404(patientRegister, id=patient_id)

                # Delete old profile image if it exists
                if patient.photo and os.path.exists(patient.photo.path):
                    os.remove(patient.photo.path)

                # Save new profile image
                photo = request.FILES["photo"]
                photo_path = f"profile_pics/{patient_id}_{photo.name}"
                patient.photo = default_storage.save(photo_path, ContentFile(photo.read()))
                
                patient.save()
                return JsonResponse({"status": "success", "message": "Image updated successfully!", "photo_url": patient.photo.url})
            
            else:
                # Process JSON Data
                data = json.loads(request.body.decode('utf-8'))
                
                patient_id = data.get("patient_id")
                if not patient_id:
                    return JsonResponse({"status": "error", "message": "Patient ID is required"})

                patient = get_object_or_404(patientRegister, id=patient_id)
                
                # Update fields
                patient.name = data.get("name", patient.name)
                patient.email = data.get("email", patient.email)
                patient.phno = data.get("phno", patient.phno)
                patient.address = data.get("address", patient.address)
                patient.city = data.get("city", patient.city)
                patient.state = data.get("state", patient.state)
                patient.blood_group = data.get("blood_group", patient.blood_group)
                patient.age = data.get("age", patient.age)
                patient.height = data.get("height", patient.height)
                patient.weight = data.get("weight", patient.weight)
                patient.dob = data.get("dob", patient.dob)

                # patient.dob = datetime.strptime(patient.dob, "%d-%m-%Y").strftime("%Y-%m-%d")

                patient.save()

                return JsonResponse({"status": "success", "message": "Patient details updated successfully!"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"})
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


import logging

# Configure logging
logger = logging.getLogger(__name__)
@ensure_csrf_cookie  # Ensures CSRF token is sent as a cookie  
def get_patient(request, patient_id):
    try:
        # Retrieve the patient object or return 404 if not found
        patient = get_object_or_404(patientRegister, id=patient_id)

        # Construct the full photo URL if the patient has an image
        photo_url = request.build_absolute_uri(settings.MEDIA_URL + patient.profile_img.name) if patient.profile_img else None

        # Prepare response data
        response_data = {
            "id": patient.id,
            "name": patient.name,
            "email": patient.email,
            "phno": patient.phno,
            "password": patient.password,  # Avoid exposing raw passwords
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
        }

        return JsonResponse(response_data)

    except AttributeError as e:
        logger.error(f"Attribute error in get_patient: {e}")
        return JsonResponse({"error": f"AttributeError: {str(e)}"}, status=500)
    
    except Exception as e:
        logger.error(f"Unexpected error in get_patient: {e}")
        return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)


def admin_profile_settings(request):
    admin_id=request.session.get('admin_id')
    if not admin_id:
        return redirect("login")
    try:
        admin=adminLogin.objects.get(id=admin_id)
        print("Admin Found",admin.username)
    except patientRegister.DoesNotExist:
        return redirect("login")
    return render(request, 'admin-profile-settings.html',{"admin":admin})


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

def admin_manage_review(request):
        all_review=review.objects.all
        return render(request, 'admin-manage-review.html',{'all':all_review})

def admin_manage_payment(request):
        all_payment=Payment.objects.all
        return render(request, 'admin-manage-payment.html',{'all':all_payment})

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




# def admin_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         try:
#             admin = adminLogin.objects.get(email=email)

#             # Check if the entered password matches the stored hashed password
#             if check_password(password, admin.password):
#                 request.session['admin_id'] = admin.id  # Store admin session
#                 return redirect('admin_dashboard')  # Ensure this matches your routes
#             else:
#                 messages.error(request, "Invalid password.")
        
#         except adminLogin.DoesNotExist:
#             messages.error(request,"Invalid email or username.")  

#     return render(request, 'admin_login.html')  # Return the login page with error messages if any

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            admin = adminLogin.objects.get(email=email)

            # Check if the entered password matches the stored hashed password
            if check_password(password, admin.password):
                request.session['admin_id'] = admin.id  # Store admin session
                messages.success(request, "Login successful! Welcome to the Admin Dashboard.")
                return redirect('admin_dashboard')  # Ensure this matches your routes
            else:
                messages.error(request, "Invalid password. Please try again.")
        
        except adminLogin.DoesNotExist:
            messages.error(request, "Invalid email or username. Please check your credentials.")

    return render(request, 'admin_login.html')  # Return the login page with error messages if any



from django.core.mail import send_mail, BadHeaderError

# def is_admin_logged_in(request):
#     return 'admin_id' in request.session

# @login_required
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



# def reject_doctor(request, doctor_id):
#     # if not is_admin_logged_in(request):
#     #     return redirect('admin_login')

#     doctor = get_object_or_404(doctorRegister, id=doctor_id)
#     doctor.is_approved = False
#     doctor.save()
#     # doctor.delete()

#     subject = 'Your Account Has Been Rejected!'
#     message = f'Hello {doctor.name}, your account has been Rejected. You can not now log in.'
#     recipient_email = doctor.email


#     try:
#         send_mail(
#             subject,
#             message,
#             'webdoctors123@gmail.com',  # Ensure this matches EMAIL_HOST_USER
#             [recipient_email],
#             fail_silently=False,
#         )
#         print(" Email sent successfully!")  # Debugging log
#     except BadHeaderError:
#         print(" Invalid email header!")
#     except Exception as e:
#         print(f" Email failed: {e}")


#     messages.error(request, f"Doctor {doctor.name} has been rejected and removed.")
#     return redirect('admin_dashboard')

def reject_doctor(request, doctor_id):
    # if not is_admin_logged_in(request):
    #     return redirect('admin_login')

    doctor = get_object_or_404(doctorRegister, id=doctor_id)
    doctor.is_approved = False
    doctor.is_rejected = True
    doctor.save()
    # doctor.delete()

    subject = 'Your Account Has Been Rejected!'
    message = f'Hello {doctor.name}, your account has been Rejected. You can not now log in.'
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


    messages.error(request, f"Doctor {doctor.name} has been rejected and removed.")
    return redirect('admin_dashboard')

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, inch




from django.http import FileResponse, HttpResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

def payment_pdf(request, payment_id):
    # Fetch payment details from the database
    try:
        payment = Payment.objects.get(id=payment_id)
        appointment = payment.appointment_id  # Assuming Payment has a ForeignKey to Appointment
        doctor = appointment.doctor_id  # Assuming Appointment has a ForeignKey to Doctor
    except Payment.DoesNotExist:
        return HttpResponse("Payment not found", status=404)

    # Create a bytestream buffer
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)

    # Page width & height
    width, height = letter

    # Set the title of the bill
    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, height - 50, "Payment Invoice")

    # Draw a horizontal line below the title
    c.line(50, height - 60, 550, height - 60)

    # Table positions
    table_x = 80
    table_y = height - 100  # **Start higher to prevent cutting**

    # **Table Title: Invoice Details**
    c.setFont("Helvetica-Bold", 14)
    c.drawString(table_x, table_y, "📌 Invoice Details")

    invoice_details = [
        ["Invoice ID:", f"{payment.id}"],
        ["Customer Name:", f"{payment.patient_id.name}"],
        ["Doctor Name:", f"Dr. {doctor.name}"],
        ["Payment Date:", f"{payment.payment_date.strftime('%Y-%m-%d')}"],
        ["Amount Paid:", f"${payment.amount:.2f}"],
        ["Payment Method:", f"{payment.payment_method}"]
    ]

    # Adjust spacing for invoice table
    invoice_table_y = table_y - 30  # **Increased spacing**

    # **Table Title: Appointment Details**
    appointment_table_y = invoice_table_y - (len(invoice_details) * 20) - 50  
    c.setFont("Helvetica-Bold", 14)
    c.drawString(table_x, appointment_table_y, "📌 Appointment Details")

    appointment_details = [
        ["Appointment ID:", f"{appointment.id}"],
        ["Appointment Date:", f"{appointment.appointment_date.strftime('%Y-%m-%d')}"],
        ["Appointment Time:", f"{appointment.appointment_time.strftime('%H:%M %p')}"],
        ["Appointment Booking Date:", f"{appointment.booking_date.strftime('%Y-%m-%d')}"]
    ]

    # Adjust spacing for appointment table
    appointment_table_y -= 30  # **More space to avoid cutoff**

    # Create and style the Invoice Table
    invoice_table = Table(invoice_details, colWidths=[180, 250])
    invoice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))

    # Create and style the Appointment Table
    appointment_table = Table(appointment_details, colWidths=[180, 250])
    appointment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))

    invoice_table.wrapOn(c, width, height)
    invoice_table.drawOn(c, table_x, invoice_table_y - (len(invoice_details) * 20))

    # ✅ **Draw Appointment Table Below Invoice Table**
    appointment_table.wrapOn(c, width, height)
    appointment_table.drawOn(c, table_x, appointment_table_y - (len(invoice_details) * 20))

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(200, 80, "Thank you for your payment!")

    # Finalize the PDF
    c.showPage()
    c.save()

    # Move buffer cursor to beginning
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="payment_invoice.pdf")

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import review  # Ensure it's imported with the correct lowercase name

def delete_review(request, review_id):
    # Get the review object or return 404 if not found
    review_obj = get_object_or_404(review, id=review_id)

    # Delete the review from the database
    review_obj.delete()

    # Show success message
    messages.success(request, "Review deleted successfully.")

    # Redirect back to the review management page
    return redirect('admin_manage_review')  # Ensure this matches your URL pattern



def delete_patient(request, patient_id):
    if request.method == 'POST':
        patient = get_object_or_404(patientRegister, id=patient_id)
        patient.delete()
        messages.success(request, 'Patient deleted successfully!')
    return redirect('admin_manage_patients')  # Redirect to the patient listing page

    # OTP sending/

    ###################
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import doctorForm  # Import your form
from .models import doctorRegister  # Import Doctor model
import random
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import requests
from django.conf import settings  # Ensure you add your API key in settings.py

MAILBOXLAYER_API_KEY = "0572de9f84c546ad0ba81a96f9090fc2"  # Replace with your actual API key
def validate_email_existence(email):
    """Check if an email exists using MailboxLayer API"""
    url = f"http://apilayer.net/api/check?access_key={MAILBOXLAYER_API_KEY}&email={email}&smtp=1&format=1"
    
    try:
        response = requests.get(url)
        data = response.json()

        # If smtp_check is True, the email exists
        if data.get("smtp_check"):
            return True
        else:
            return False
    except requests.RequestException:
        return False    
    
def doctor_register(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            validate_email(email)  # Check if email format is correct
        except ValidationError:
            messages.error(request, "Invalid email address format. Please enter a valid email.")
            return redirect('doctor_register')

        #  Check if email already exists
        if doctorRegister.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered. Try logging in.")
            return redirect('doctor_register')

            #  Validate if the email actually exists
        if not validate_email_existence(email):
            messages.error(request, "Email address does not exist. Please enter a valid email.")
            return redirect('doctor_register')

        #  If email is new, proceed with storing data temporarily
        form = doctorForm(request.POST, request.FILES)

        if form.is_valid():
            
            password = form.cleaned_data.get('password')
            if not password:
                messages.error(request, "Password is required!")
                return redirect('doctor_register')
            # Store form data in session (excluding password)
            doctor_data = form.cleaned_data
            doctor_data.pop('password')  # Exclude password for security
            request.session['doctor_data'] = doctor_data
            request.session['doctor_password'] = make_password(password)  # Store hashed password
            doctor_data['fee'] = doctor_data.get('fee', 0)  # If fee is missing, set it to 0


            # Generate OTP for email verification
            otp = random.randint(100000, 999999)
            print(f"Generated OTP: {otp}")  #  Print OTP in terminal

            request.session['otp'] = otp  # Store OTP in session
            request.session['email'] = email  # Store email in session

            # Send OTP email
            subject = "Email Verification OTP"
            message = f"Your OTP for doctor registration is: {otp}. Do not share this with anyone."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(request, "OTP sent to your email. Please verify.")
            return redirect('verify_otp', email=email)  # Redirect to OTP verification page

        else:
            messages.error(request, "Invalid form submission. Please check your details.")

    else:
        form = doctorForm()

    return render(request, 'doctor-register.html', {'form': form})

def verify_otp(request, email):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get('otp')
        if stored_otp and int(entered_otp) == stored_otp:
            # Retrieve stored doctor data from session
            doctor_data = request.session.get('doctor_data')
            doctor_password = request.session.get('doctor_password')

            if doctor_data and doctor_password:
                # Save doctor to database
                doctor = doctorRegister(**doctor_data)
                doctor.password = doctor_password  # Assign hashed password
                doctor.save()

                # Remove OTP and session data
                del request.session['otp']
                del request.session['doctor_data']
                del request.session['doctor_password']

                messages.success(request, "Registration successful! You can now log in.")
                return redirect('login')
            else:
                messages.error(request, "Session expired. Please register again.")
                return redirect('doctor_register')

        else:
            messages.error(request, "Invalid OTP! Please try again.")

    return render(request, 'verify_otp.html', {'email': email})

#####################################

def patient_register(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            validate_email(email)  # Check if email format is correct
        except ValidationError:
            messages.error(request, "Invalid email address format. Please enter a valid email.")
            return redirect('patient_register')

        if patientRegister.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered. Try logging in.")
            return redirect('patient_register')

                    # ✅ Validate if the email actually exists
        if not validate_email_existence(email):
            messages.error(request, "Email address does not exist. Please enter a valid email.")
            return redirect('patient_register')
        
        form = patientForm(request.POST, request.FILES)

        if form.is_valid():
            password = form.cleaned_data.get('password')
            if not password:
                messages.error(request, "Password is required!")
                return redirect('patient_register')
            
            patient_data = form.cleaned_data
            patient_data.pop('password')  # Exclude password for security
            request.session['patient_data'] = patient_data
            request.session['patient_password'] = make_password(password)  # Store hashed 

                        # Generate OTP for email verification
            otp = random.randint(100000, 999999)
            print(f"Generated OTP: {otp}")  # ✅ Print OTP in terminal

            request.session['otp'] = otp  # Store OTP in session
            request.session['email'] = email  # Store email in session

                        # Send OTP email
            subject = "Email Verification OTP"
            message = f"Your OTP for doctor registration is: {otp}. Do not share this with anyone."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(request, "OTP sent to your email. Please verify.")
            return redirect('verify_otp_patient', email=email)  # Redirect to OTP verification page
        else:
            messages.error(request, "Invalid form submission. Please check your details.")
    else:
        form = patientForm()
    return render(request, 'patient-register.html', {'form': form})


def verify_otp_patient(request, email):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get('otp')

        if stored_otp and int(entered_otp) == stored_otp:
            # Retrieve stored doctor data from session
            patient_data = request.session.get('patient_data')
            patient_password = request.session.get('patient_password')

            if patient_data and patient_password:
                # Save doctor to database
                patient = patientRegister(**patient_data)
                patient.password = patient_password  # Assign hashed password
                patient.save()

                # Remove OTP and session data
                del request.session['otp']
                del request.session['patient_data']
                del request.session['patient_password']

                messages.success(request, "Registration successful! You can now log in.")
                return redirect('login')
            else:
                messages.error(request, "Session expired. Please register again.")
                return redirect('patient_register')

        else:
            messages.error(request, "Invalid OTP! Please try again.")

    return render(request, 'verify_otp_patient.html', {'email': email})