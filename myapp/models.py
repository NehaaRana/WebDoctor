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

      address = models.TextField()  # Full address
      city = models.CharField(max_length=50)
      state = models.CharField(max_length=50)
      pincode = models.IntegerField(), 
      country = models.CharField(max_length=50),
      blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)  # Dropdown selection
  
      # def __str__(self):
      #     return f"{self.name} | {self.email} | {self.phno} | {self.password} | {self.profile_img.url if self.profile_img else 'No Image'} | {self.address} | {self.city} | {self.state} | {self.pincode} | {self.country} | {self.blood_group}"
      def __str__(self):
        return f"{self.name} | {self.email} | {self.phno}"
      