from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from .forms import patientForm
from .models import patientRegister
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

def login(request):
         return render(request, 'login.html')

def search_doctors(request):
         return render(request, 'search.html')

def patient_dashboard(request):
         return render(request, 'patient-dashboard.html')

def doctor_dashboard(request):
         return render(request, 'doctor-dashboard.html')

def admin_dashboard(request):
         return render(request, 'admin-dashboard.html')
def doctor_register(request):
         return render(request, 'doctor-register.html')

def patient_register(request):
    if request.method == "POST":
        form = patientForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect instead of rendering login page directly
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

def book_appointment(request):
    return render(request, 'booking.html')

def doctor_change_password(request):
    return render(request, 'doctor-change-password.html')

def patient_change_password(request):
    return render(request, 'patient-change-password.html')

def password_change_successful(request):
    return render(request, 'password-change-successful.html')

def verify(request):
    return render(request, 'verify.html')
      