from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator

class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(validators=[RegexValidator(r'^\d+$', message="Phone number must be all digits.")],max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name','password']

class SpamNumbers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(validators=[RegexValidator(r'^\d+$', message="Phone number must be all digits.")],max_length=15)
    count = models.IntegerField(default=0)
    
class Contacts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

# class SearchHistory(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
#     query = models.CharField(max_length=255)
#     timestamp = models.DateTimeField(auto_now_add=True)