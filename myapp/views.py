from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from .forms import patientForm,doctorForm,passwordChangeForm
from .models import patientRegister,doctorRegister
# #####################################
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
# Create your views here.
# from django.shortcuts import render

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

        if user_type == "patient":
            try:
                user = patientRegister.objects.get(email=email)
                request.session['patient_id'] = user.id  # Store in session
                print(f"Patient found: {user.email}")
            except patientRegister.DoesNotExist:
                print("Patient does not exist")
                return render(request, "login.html", {"error": "Patient does not exist"})

        elif user_type == "doctor":
            try:
                user = doctorRegister.objects.get(email=email)
                request.session['doctor_id'] = user.id  # Store in session
                print(f"Doctor found: {user.email}")
            except doctorRegister.DoesNotExist:
                print("Doctor does not exist")
                return render(request, "login.html", {"error": "Doctor does not exist"})

        else:
            print("Invalid user type")
            return render(request, "login.html", {"error": "Invalid user type"})

        # ✅ **Compare hashed password using check_password()**
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


# def doctor_register(request):
#     if request.method == "POST":
#         form = doctorForm(request.POST, request.FILES)  # Handle file uploads
#         if form.is_valid():
#             print("Form is valid, saving the data.")  # Debug print
#             doctor = form.save(commit=False)  # Don't save yet
#             doctor.password = make_password(form.cleaned_data["password"])  # Hash password
#             doctor.save()         
#             return redirect('login')  # Redirect instead of rendering login page directly
#         else:
#             print("Form errors:", form.errors)  # Debug print
#     else:
#         form = doctorForm()  # Create an empty form for GET request

#     return render(request, 'doctor-register.html', {'form': form})  # Pass form to template


# def patient_register(request):

#     if request.method == "POST":
#         form = patientForm(request.POST, request.FILES)  # Handle file uploads
#         if form.is_valid():
#             patient = form.save(commit=False)  # Don't save yet
#             patient.password = make_password(form.cleaned_data["password"])  # Hash password
#             patient.save()
#             return redirect('login')  # Redirect instead of rendering login page directly
#         else:
#             print("Form errors:", form.errors)  # Debug print
            
#     else:
#         form = patientForm()  # Create an empty form for GET request

#     return render(request, 'patient-register.html', {'form': form})  # Pass form to template

def doctor_register(request):
    if request.method == "POST":
        form = doctorForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.password = make_password(doctor.password)  # 🔒 Hash the password before saving
            doctor.save()
            return redirect('login')
    else:
        form = doctorForm()
    return render(request, 'doctor-register.html', {'form': form})

def patient_register(request):
    if request.method == "POST":
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

def book_appointment(request):
    return render(request, 'booking.html')

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
#     patient_id = request.session.get('patient_id')  # Get user ID from session
    
#     if not patient_id:
#         return redirect("login")  # Redirect to login if session is empty
    
#     try:
#         patient = patientRegister.objects.get(id=patient_id)  # Fetch patient data
#         print("Patient Found:", patient.name)  # Debugging
#     except patientRegister.DoesNotExist:
#         return redirect("login")
#     return render(request, 'patient-change-password.html',{"patient": patient})

def patient_change_password(request):
    patient_id = request.session.get('patient_id')  # Get logged-in patient ID
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

    return render(request, "patient-change-password.html",{"patient":patient,"form":form})


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
@csrf_exempt
def update_doctor(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))  # Ensure JSON decoding

            # Use session ID as a fallback
            doctor_id = data.get("doctor_id", request.session.get('doctor_id'))
            if not doctor_id:
                return JsonResponse({"status": "error", "message": "Doctor ID is required"})

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

            return JsonResponse({"status": "success", "message": "Doctor details updated successfully!"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method"})


@ensure_csrf_cookie  # Ensures CSRF token is sent as a cookie
def get_doctor(request, doctor_id):
    doctor = get_object_or_404(doctorRegister, id=doctor_id)
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
        "csrfToken": get_token(request)  # Send CSRF token in response
    })


####################################update patient
@csrf_exempt
def update_patient(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))  # Ensure JSON decoding

            # Use session ID as a fallback
            patient_id = data.get("patient_id", request.session.get('patient_id'))
            if not patient_id:
                return JsonResponse({"status": "error", "message": "patient ID is required"})

            patient = get_object_or_404(patientRegister, id=patient_id)

            # Update fields
            patient.name = data.get("name", patient.name)
            patient.email = data.get("email", patient.email)
            patient.phno = data.get("phno", patient.phno)
            patient.password=data.get("password",patient.password)
            patient.address = data.get("address", patient.address)
            patient.city = data.get("city", patient.city)
            patient.state = data.get("state", patient.state)
            patient.blood_group = data.get("blood_group", patient.blood_group)
            patient.age = data.get("age", patient.age)
            patient.height = data.get("height", patient.height)
            patient.weight = data.get("weight", patient.weight)
            patient.dob = data.get("dob", patient.dob)


            patient.save()  # Save changes

            return JsonResponse({"status": "success", "message": "patient details updated successfully!"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method"})


@ensure_csrf_cookie  # Ensures CSRF token is sent as a cookie
def get_patient(request, patient_id):
    patient = get_object_or_404(patientRegister, id=patient_id)
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
        "csrfToken": get_token(request)  # Send CSRF token in response
    })
