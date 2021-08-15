from django.db import models

# Create your models here.
class CharityUser(models.Model):
    username = models.CharField(max_length = 100,primary_key = True) # Charity User_Name
    name = models.CharField(max_length = 100) # Charity Name
    description = models.TextField() # Short Description about Charity
    image = models.CharField(max_length=100)  # Path of Iamge
    donors = models.IntegerField(default=0) # No of donors Donated
    amount = models.IntegerField(default=0) # Total Amount of Doantion Made
    def __str__(self):
        return self.name

class Donor(models.Model):
    username = models.CharField(max_length = 100) #UserName of Donor
    amount = models.IntegerField(default=0) # Amout Donated
    charityusername = models.CharField(max_length = 100) # Charity User Name to which it is donated

    def __str__(self):
        return self.username

class Contact(models.Model):
    name = models.CharField(max_length = 100) #Name of Person
    email = models.CharField(max_length = 100) #Email of Person
    message = models.TextField()

    def __str__(self):
        return self.name