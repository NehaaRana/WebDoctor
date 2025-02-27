from django.urls import path
from . import views

urlpatterns =[
  path("",views.home,name="home"),
  path('about_us/', views.about_us, name='about_us'),
  path('about/', views.about, name='about'),
  path('contact/', views.contact, name='contact'),
  path('contact_us/', views.contact_us, name='contact_us'),
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  path('search_doctors/', views.search_doctors, name='search_doctors'),
  path('index/', views.index, name='index'),
  path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
  path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
  path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
  path('contact_us/', views.contact_us, name='contact_us'),
  path('logout/', views.logout_view, name='logout'), 
  path('coming-soon/', views.coming_soon, name='coming-soon'),
  path('subscribe/', views.subscribe, name='subscribe'),
  path('terms-condition/', views.terms_condition, name='terms-condition'),
  path('doctor_register/', views.doctor_register, name='doctor_register'),
  path('patient_register/', views.patient_register, name='patient_register'),
  path('terms_condition/', views.terms_condition, name='terms_condition'),
  path('patient_profile/', views.patient_profile, name='patient_profile'),
  path('doctor_profile/<int:doctor_id>/', views.doctor_profile, name='doctor_profile'),
  # path('book_appointment/<int:doctor_id>/<int:appointment_id>/', views.book_appointment, name='book_appointment'),
  path('doctor_profile/<int:doctor_id>/', views.doctor_profile, name='doctor_profile'),
  # path('book_appointment/<int:doctor_id>/<int:appointment_id>/', views.book_appointment, name='book_appointment'),
  path('doctor_profile_settings/', views.doctor_profile_settings, name='doctor_profile_settings'),
  path('book_appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
  path('book_appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
  path('doctor_change_password/', views.doctor_change_password, name='doctor_change_password'),
  path('patient_change_password/', views.patient_change_password, name='patient_change_password'),
  path('password_change_successful/', views.password_change_successful, name='password_change_successful'),
  path('verify/', views.verify, name='verify'),
  path('patient_profile_settings/', views.patient_profile_settings, name='patient_profile_settings'),
  path('search/', views.search, name='search'),

  ########################
   path('update-doctor/', views.update_doctor, name='update_doctor'),
    path('get-doctor/<int:doctor_id>/',views.get_doctor, name='get_doctor'),
       path('update-patient/', views.update_patient, name='update_patient'),
    path('get-patient/<int:patient_id>/',views.get_patient, name='get_patient'),
  path('payment_details/<int:appointment_id>/<int:doctor_id>/', views.payment_details, name='payment_details'),

  path('admin_login/',views.admin_login, name='admin_login'),
  path('admin_profile_settings/', views.admin_profile_settings, name='admin_profile_settings'),
  path('admin_change_password/', views.admin_change_password, name='admin_change_password'),
  path('admin_manage_docters/',views.admin_manage_docters,name='admin_manage_doctors'),
  path('admin_manage_patients/',views.admin_manage_patients,name='admin_manage_patients'),
  path('admin_manage_appointments/',views.admin_manage_appointments,name='admin_manage_appointments'),
  path('admin_logout/', views.admin_logout, name='admin_logout'),

  ########################
   path('update-doctor/', views.update_doctor, name='update_doctor'),
    path('get-doctor/<int:doctor_id>/',views.get_doctor, name='get_doctor'),
       path('update-patient/', views.update_patient, name='update_patient'),
  path('get-patient/<int:patient_id>/',views.get_patient, name='get_patient'),

  path('payment/<int:appointment_id>/<int:doctor_id>/', views.payment_page, name='payment'),
  path('payment_details/<int:appointment_id>/<int:doctor_id>/', views.payment_details, name='payment_details'),

]
