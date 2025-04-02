from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class patientRegister(models.Model):
      BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')
      ]
      
      name = models.CharField(max_length=100)
      email = models.EmailField(unique=True)
      phno = models.BigIntegerField(unique=True) 
      password = models.CharField(max_length=255)
      profile_img = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
      dob=models.DateField(null=True)
      age = models.PositiveIntegerField(null=True)  # Age field
      weight = models.DecimalField(null=True,max_digits=5,decimal_places=2)#Weight field
      height = models.DecimalField(null=True,max_digits=5, decimal_places=2) 
      address = models.TextField()  # Full address
      city = models.CharField(max_length=50)
      state = models.CharField(max_length=50)
      blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)  # Dropdown selection

      def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

      def check_password(self, raw_password):
        return check_password(raw_password, self.password)
      

      def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

      def check_password(self, raw_password):
        return check_password(raw_password, self.password)
     
     
      def __str__(self):
        return f"{self.name} | {self.email} | {self.phno}"
      
class doctorRegister(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    AVAILABILITY_CHOICES = [
        ('Available', 'Available'),
        ('Not Available', 'Not Available'),
   
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phno = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=100)
    profile_img = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    qualification = models.CharField(max_length=100,blank=True, null=True)
    specialization = models.CharField(max_length=100,blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50,blank=True, null=True)
    state = models.CharField(max_length=50,blank=True, null=True)
    clinic_name = models.CharField(max_length=255)
    clinic_address = models.TextField() 
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    mci_no = models.CharField(max_length=10,blank=True, null=True)
    fee = models.BigIntegerField(null=True)
    about_me=models.TextField(null=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_available = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES)  # Updated field


    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
            return f"{self.name} | {self.gender} |{self.email} | {self.password} | {self.qualification} |{self.specialization} | {self.phno} | "
    
class appointment(models.Model):
     STATUS_CHOICE=[('Pending', 'Pending'), ('Confirm', 'Confirm'), ('Cancelled', 'Cancelled')]
     doctor_id=models.ForeignKey(doctorRegister,on_delete=models.CASCADE)
     patient_id=models.ForeignKey(patientRegister,on_delete=models.CASCADE)
     appointment_date = models.DateField() 
     appointment_time = models.TimeField()
     reason = models.TextField(null=True)
     symptoms = models.CharField(max_length=255, blank=True, null=True)
     status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='Pending') 
     reason = models.TextField(null=True)
     symptoms = models.CharField(max_length=255, blank=True, null=True)
     booking_date = models.DateField(default=now)
     meeting_link = models.URLField(blank=True, null=True)


     def __str__(self):
          return f"{self.appointment_date} | {self.appointment_time} | {self.reason} | {self.symptoms} | {self.booking_date} | "

class review(models.Model):
      patient_id=models.ForeignKey(patientRegister,on_delete=models.CASCADE)
      doctor_id=models.ForeignKey(doctorRegister,on_delete=models.CASCADE)
      appointment_id=models.ForeignKey(appointment,on_delete=models.CASCADE)
      rating=models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
      review_text=models.TextField(blank=True, null=True)
      review_date=models.DateField()

      def __str__(self):
          return f"{self.rating} | {self.review_text} | {self.review_date} |"



import uuid
from django.db import models

class Payment(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    METHOD_CHOICES = [
        ('CARD', 'Debit/Credit Card'),
        ('BANK', 'Bank Transfer'),
        ('UPI', 'UPI'),
    ]

    patient_id = models.ForeignKey(patientRegister, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(doctorRegister, on_delete=models.CASCADE)
    appointment_id = models.ForeignKey(appointment, on_delete=models.CASCADE)

    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.TextField(blank=True, null=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='CARD')
    payment_date = models.DateTimeField(auto_now_add=True)  # Automatically sets the date

    def save(self, *args, **kwargs):
        if not self.razorpay_order_id:
            # Ensure the generated ID is unique before assigning
            unique_order_id = str(uuid.uuid4())
            while Payment.objects.filter(razorpay_order_id=unique_order_id).exists():
                unique_order_id = str(uuid.uuid4())  # Generate a new UUID if duplicate exists
            self.razorpay_order_id = unique_order_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.amount} | {self.payment_status} | {self.payment_method} | {self.payment_date}"

class adminLogin(models.Model):
    username = models.CharField(max_length=150, unique=True,default="null")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Store hashed password using Django's authentication2

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.username
        

class HealthRecord(models.Model):
    patient = models.ForeignKey(patientRegister, on_delete=models.CASCADE)
    bp_systolic = models.IntegerField(null=True, blank=True)
    bp_diastolic = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)  # New
    sugar_level = models.FloatField(null=True, blank=True)
    steps_walked = models.IntegerField(null=True, blank=True)  # New
    sleep_hours = models.FloatField(null=True, blank=True)  # New
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Health Record for {self.patient} on {self.recorded_at}"
    


from datetime import date
class Prescription(models.Model):
    doctor = models.ForeignKey(doctorRegister, on_delete=models.CASCADE, related_name="doctor_prescriptions")
    patient = models.ForeignKey(patientRegister, on_delete=models.CASCADE, related_name="patient_prescriptions")
    date_issued = models.DateField(default=date.today)
    medicines = models.TextField()  # Store medicine details in JSON format or simple text
    diagnosis = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return f"Prescription {self.id} - {self.patient.username}"
    

class EmergencyRequest(models.Model):
    patient = models.ForeignKey(
        patientRegister, on_delete=models.CASCADE, related_name="emergencies", null=True, blank=True
    )
    doctor = models.ForeignKey(
        doctorRegister, on_delete=models.SET_NULL, null=True, blank=True, related_name="emergency_cases"
    )  # Doctor assigned for emergency consultation

    meeting_link = models.URLField(max_length=500, null=True, blank=True)  # Store video call link

    created_at = models.DateTimeField(auto_now_add=True)  # When request was made
    updated_at = models.DateTimeField(auto_now=True)  # Track last update

    def __str__(self):
        doctor_name = self.doctor.name if self.doctor else "Unknown Doctor"
        patient_name = self.patient.name if self.patient else "Unknown Patient"
        
        return f"Emergency request with {doctor_name} by {patient_name}"  # Always returns a string



class Medicine(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Discontinued', 'Discontinued'),
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    manufacturer = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(default=now) 
    img = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


    def _str_(self):
        return self.name
    

class Order(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(patientRegister, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payer_email = models.EmailField()
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed')
    ])
    created_at = models.DateTimeField(auto_now_add=True)