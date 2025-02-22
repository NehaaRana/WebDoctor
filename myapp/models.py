from django.db import models

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

      address = models.TextField(null=True, blank=True)  # Temporarily allow null values
      city = models.CharField(max_length=50)
      state = models.CharField(max_length=50)
      pincode = models.IntegerField(), 
      country = models.CharField(max_length=50),
      blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)  # Dropdown selection
  
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
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    clinic_name = models.CharField(max_length=255)
    clinic_address = models.TextField()
    email = models.EmailField(unique=True)
    phno = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=100)
    profile_img = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    qualification = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    address = models.TextField(null=True, blank=True)  # Temporarily allow null values
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    mci_no = models.CharField(max_length=10)

    def __str__(self):
            return f"{self.name} | {self.gender}| {self.clinic_name} |{self.clinic_address} |{self.email} | {self.phno}| {self.password} | "      