from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Password(models.Model):
    user = models.ForeignKey(User, related_name="User", on_delete=models.CASCADE)
    website_name = models.CharField(max_length=255)
    website_url = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_compromised = models.BooleanField(default=False)
    expiration_date = models.DateField(null=True, blank=True)
    sharing_token = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.website_name
    

class Setting(models.Model):

    class Period(models.IntegerChoices):
        DEFAULT = 1, "" 
        DAYS = 2, "DAYS"
        MONTHS = 3, "MONTHS"
        YEARS = 4, "YEARS"

    user =  models.ForeignKey(User, related_name="Settings_User", on_delete=models.CASCADE)
    share_passwords = models.BooleanField(default=False)
    expire_number = models.IntegerField()
    expire_period = models.PositiveSmallIntegerField(choices=Period.choices, default=Period.DEFAULT, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PasswordSharing(models.Model):

    owner =  models.ForeignKey(User, related_name="Password_Owner", on_delete=models.CASCADE)
    tenant =  models.ForeignKey(User, related_name="Password_Tenant", on_delete=models.CASCADE)
    password =  models.ForeignKey(Password, related_name="Concerned_Password", on_delete=models.CASCADE)
    valid_until =  models.DateField(default="", blank=True, null=True)
    owner_authorize = models.BooleanField(default=False) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CompromisedSite(models.Model):

    website_name = models.CharField(max_length=255)
    website_url = models.CharField(max_length=255)  
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

