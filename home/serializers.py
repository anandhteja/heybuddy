from rest_framework import serializers

from django.contrib.auth.models import User
from home.models import Contactdeveloper




class Userserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username',)



class Contactdeveloperserializer(serializers.ModelSerializer):
    class Meta:
        model=Contactdeveloper
        fields='__all__'