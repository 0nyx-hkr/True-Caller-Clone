# api/serializers.py
from rest_framework import serializers
from .models import User
from django.core.validators import RegexValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone_number', 'email','password']  
        extra_kwargs = {
            'password' : {'write_only':True}
        }
    def create(self,validate_data):
        password = validate_data.pop('password',None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class SpamNumberSerializer(serializers.Serializer):
    phone_number = phone_number = serializers.CharField(validators=[RegexValidator(r'^\d+$', message="Phone number must be all digits.")],max_length = 255)

class SearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=255)
