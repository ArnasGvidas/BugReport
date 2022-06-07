from django.db import models

class userdata(models.Model):
    E_Mail=models.CharField(max_length=200)
    Username=models.CharField(max_length=200)
    Password=models.CharField(max_length=200)
    IsEmploye=models.IntegerField(default=0)
class customer(models.Model):
    FirstName=models.CharField(max_length=200)
    LastName=models.CharField(max_length=200)
    UID=models.OneToOneField(userdata,
        on_delete=models.CASCADE,
        primary_key=True)
class problem(models.Model):
    Customer=models.ForeignKey(customer, on_delete=models.CASCADE)
    Topic=models.CharField(max_length=200)
    Description=models.CharField(max_length=200)
    Status=models.CharField(max_length=200)