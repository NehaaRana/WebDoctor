from django.urls import path
from . import views

urlpatterns = [
  path("",views.home,name="home"),
  path('about_us/', views.about_us, name='about_us'),
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
  path('terms_condition/', views.terms_condition, name='terms_condition')
  

]
