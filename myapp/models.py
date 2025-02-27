from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.hashers import make_password, check_password

from django.core.validators import MinValueValidator, MaxValueValidator
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
      
      # pincode = models.IntegerField(null=True) 
      # country = models.CharField(max_length=50,null=True)
      # def __str__(self):
      #     return f"{self.name} | {self.email} | {self.phno} | {self.password} | {self.profile_img.url if self.profile_img else 'No Image'} | {self.address} | {self.city} | {self.state} | {self.pincode} | {self.country} | {self.blood_group}"
     
     
      def __str__(self):
        return f"{self.name} | {self.email} | {self.phno}"
      
class doctorRegister(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
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

    # class Meta:
    #     db_table = 'myapp_doctorregister'  # Explicitly link to the existing table
    #     managed = True  # 🚨 Change this to True so Django can manage the table
    def __str__(self):
            return f"{self.name} | {self.gender} |{self.email} | {self.password} | {self.clinic_name} |{self.clinic_address} | {self.phno} | "
    
class appointment(models.Model):
    #  STATUS_CHOICE=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')]
    #  STATUS_CHOICE=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')]
     doctor_id=models.ForeignKey(doctorRegister,on_delete=models.CASCADE)
     patient_id=models.ForeignKey(patientRegister,on_delete=models.CASCADE)
     appointment_date = models.DateField() 
     appointment_time = models.TimeField()
    #  status= models.CharField(max_length=20,choices=STATUS_CHOICE,default='Scheduled')
     reason = models.TextField(null=True)
     symptoms = models.CharField(max_length=255, blank=True, null=True)
    #  status= models.CharField(max_length=20,choices=STATUS_CHOICE,default='Scheduled')
     reason = models.TextField(null=True)
     symptoms = models.CharField(max_length=255, blank=True, null=True)

     def __str__(self):
          return f"{self.appointment_date} | {self.appointment_time} | {self.reason} | {self.symptoms} |"

class review(models.Model):
      patient_id=models.ForeignKey(patientRegister,on_delete=models.CASCADE)
      doctor_id=models.ForeignKey(doctorRegister,on_delete=models.CASCADE)
      appointment_id=models.ForeignKey(appointment,on_delete=models.CASCADE)
      rating=models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
      review_text=models.TextField(blank=True, null=True)
      review_date=models.DateField()

      def __str__(self):
          return f"{self.rating} | {self.review_text} | {self.review_date} |"


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
      patient_id=models.ForeignKey(patientRegister,on_delete=models.CASCADE)
      doctor_id=models.ForeignKey(doctorRegister,on_delete=models.CASCADE)
      appointment_id=models.ForeignKey(appointment,on_delete=models.CASCADE)
      amount = models.DecimalField(max_digits=10, decimal_places=2)
      payment_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
      payment_method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='CARD')
      payment_date = models.DateTimeField() 

      def __str__(self):
          return f"{self.amount} | {self.payment_status} | {self.payment_method} | {self.payment_date} |"

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
        

class review(models.Model):
      patient_id=models.ForeignKey(patientRegister,on_delete=models.CASCADE)
      doctor_id=models.ForeignKey(doctorRegister,on_delete=models.CASCADE)
      appointment_id=models.ForeignKey(appointment,on_delete=models.CASCADE)
      rating=models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
      review_text=models.TextField(blank=True, null=True)
      review_date=models.DateField()

      def __str__(self):
          return f"{self.rating} | {self.review_text} | {self.review_date} |"

