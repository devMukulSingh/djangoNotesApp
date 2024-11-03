from django.shortcuts import render,redirect
from rest_framework import generics
from .serializers import UserSerializers,LoginSerializer
from django.contrib import messages
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate,login,logout  
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token

class SignUpUser(APIView) : 
    
    serializer_class = UserSerializers

    def post(self,request) : 
        data = request.data
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if User.objects.filter( email = email) : 
           return Response(status=400,data={"error":"User already exists"})
        user = User.objects.create(
            email = email,
            password = password,
            username = name
        )
        user.set_password(password)
        user.save()
        
        serializer = UserSerializers(user)
        return Response(status=201,data={
            "message":"user created",
            "data":serializer.data
        })
    
class SignInUser(APIView): 

    def post(self,request) : 

        data = request.data
        serializer  = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response(status=400,data={
                'error':serializer.errors
            })
        print(serializer.data)
        username = serializer.data['username']
        password = serializer.data['password']
        user_obj = authenticate(username=username,password=password)
        
        print(user_obj)
        if user_obj is None: 
            return Response(
                status=400,
                data={
                      "error":"Invalid credentials",
                }
            )
        
        token, created = Token.objects.get_or_create(user=user_obj)
        return Response(
            status=200,
            data={
                "message":"Login sucess",
                "data":token.key
            }
        )


    