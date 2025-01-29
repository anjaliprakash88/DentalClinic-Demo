from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


#-------------USER MODEL-------------------------#
class User(AbstractUser):
    is_superadmin=models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_pharmacy = models.BooleanField(default=False)
    is_reception = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Branch(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    email_address = models.EmailField(null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name


# -------------------------DOCTOR MODEL--------------------------------------------
class Doctor(models.Model):
    user = models.OneToOneField(User, related_name="doctor", on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, related_name="doctors", on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100,
                                      choices=[('General Dentist', 'General Dentist'),
                                               ('Orthodontist', 'Orthodontist'),
                                               ('Periodontist', 'Periodontist'),
                                               ('Endodontist', 'Endodontist'),
                                               ('Prosthodontist', 'Prosthodontist')])
    experience_years = models.PositiveIntegerField()
    qualification = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)


# ---------------------- Pharmacy Model ----------------------
class Pharmacy(models.Model):
    user = models.OneToOneField(User, related_name="pharmacy", on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, related_name="pharmacys", on_delete=models.CASCADE)
    experience_years = models.PositiveIntegerField()
    qualification = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

# ------------------------Receptionist----------------------------------
class Receptionist(models.Model):
    user = models.OneToOneField(User, related_name="receptionist", on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, related_name="receptionists", on_delete=models.CASCADE)
    experience_years = models.PositiveIntegerField()
    qualification = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username