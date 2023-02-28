# import json
# from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import serializers
from . models import *
from rest_framework import status
# from django.db.models import Q
# import re


#Account serialzer
class AccountSerializer(serializers.ModelSerializer):

    #for confirmation password
    password2 = serializers.CharField(
        style={'input': 'password'}, write_only=True)
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        expect="password"
        fields = ['username', 'email', 'password', 'password2' ]
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        register = Account(
            username    =   self.validated_data["username"],
            email       =   self.validated_data["email"],
        )
        password=self.validated_data["password"]
        password2=self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({'password':'password dosent match'})
        
        register.set_password(password)
        print("jjjjjjjjjjjjjj")
        register.save()
        return register
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields=  '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedTasks
        fields=  '__all__'
        depth = 1


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apps
        fields=  '__all__'   


class CompletedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedTasks
        fields=  '__all__' 