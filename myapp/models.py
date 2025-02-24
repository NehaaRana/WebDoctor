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
      age = models.PositiveIntegerField(null=True)  # Age field
      weight = models.DecimalField(null=True,max_digits=5,decimal_places=2)#Weight field
      height = models.DecimalField(null=True,max_digits=5, decimal_places=2) 
      address = models.TextField()  # Full address
      city = models.CharField(max_length=50)
      state = models.CharField(max_length=50)
      blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)  # Dropdown selection
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

    # class Meta:
    #     db_table = 'myapp_doctorregister'  # Explicitly link to the existing table
    #     managed = True  # 🚨 Change this to True so Django can manage the table
    def __str__(self):
            return f"{self.name} | {self.gender} |{self.email} | {self.password} | {self.clinic_name} |{self.clinic_address} | {self.phno} | "
