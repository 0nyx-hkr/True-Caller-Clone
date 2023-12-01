from django.contrib import admin
from .models import User,Contacts,SpamNumbers

admin.site.register(User)
admin.site.register(Contacts)
admin.site.register(SpamNumbers)
# Register your models here.
