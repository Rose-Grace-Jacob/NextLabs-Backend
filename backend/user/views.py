from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.decorators import api_view, permission_classes
# from django.db.models import Q
from rest_framework import status
from . models import *
from . serializers import *
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework import permissions
# from rest_framework.generics import ListAPIView

# Create your views here.


class SignupView(APIView):
    def post(self, request):

        user=request.data
        serializer=AccountSerializer(data=request.data)
        datas={}
        if serializer.is_valid():
            acc = serializer.save()
            if acc:
                return Response(status=status.HTTP_201_CREATED)
            else:
                print('Error',acc)    
        else:
            if Account.objects.get(username=user['username']):
                datas["error"]={"Username is already present"} 
                return Response(datas,status=status.HTTP_205_RESET_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            user=request.user
            user_data= Account.objects.filter(username=user)
            print(user_data)
            userserializer = UserProfileSerializer(user_data,many=True)
            print(userserializer.data)
            if userserializer.is_valid: 
                return Response(userserializer.data,status=status.HTTP_200_OK)
            else:
                return Response(userserializer.errors,status=status.HTTP_404_NOT_FOUND)

        except:
            return Response(userserializer.errors,status=status.HTTP_404_NOT_FOUND)
        

class UserTask(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer=None
        u_data={}
        try:
            user=request.user
            user_data= CompletedTasks.objects.filter(users=user.id)
            print(user_data)
           
            serializer = TaskSerializer(user_data,many=True)
            if serializer.is_valid:
                return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    

class Showapp(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer=None
        try:
            app_data = Apps.objects.all()
            serializer = AppSerializer(app_data, many = True)
            if serializer.is_valid: 
                return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
        

class Completetask(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes=(MultiPartParser, FormParser)
    def post(self,request):
        print(request.data)
        value = request.data
        tasks = CompletedTaskSerializer(data=request.data)
        if tasks.is_valid():
            tasks.save()
            user = request.user
            app = Apps.objects.get(id=value["app"])
            print(app)
            user.user_points = int(user.user_points) + int(app.points)
            user.save()
            return Response(status=200)
        else:
            data = tasks.errors
            return Response(data,status=status.HTTP_404_NOT_FOUND)
        

class Addapp(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        task=None
        data={}
        try:
            user=user=request.user
            if user.is_superadmin:
                task=AppSerializer(data=request.data)
                if task.is_valid():
                    task.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(datastatus=status.HTTP_403_FORBIDDEN)
        except:
            return Response(data,status=status.HTTP_403_FORBIDDEN)
        

class Adminapps(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        task=None
        
        try:
            user=request.user
            if user.is_superadmin:
                print(user.id)
                app_data = Apps.objects.filter(creator=user.id)
                task = AppSerializer(data=app_data,many=True)
                task.is_valid()
                return Response(task.data,status=status.HTTP_200_OK)
        except:
            return Response(task.errors,status=status.HTTP_403_FORBIDDEN)