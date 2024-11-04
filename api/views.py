from django.shortcuts import render,redirect
from rest_framework import generics,status
from .serializers import UserSerializers,LoginSerializer,NotesSerializer,NoteSerializer
from django.contrib import messages
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate,login,logout  
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from .models import Note
from rest_framework.authentication import TokenAuthentication

class SignUpUser(APIView) : 
    
    serializer_class = UserSerializers

    def post(self,request) : 
        data = request.data
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if User.objects.filter( email = email) : 
           return Response(status=status.HTTP_400_BAD_REQUEST,data={"error":"User already exists"})
        user = User.objects.create(
            email = email,
            password = password,
            username = name
        )
        user.set_password(password)
        user.save()
        
        serializer = UserSerializers(user)
        return Response(status=status.HTTP_201_CREATED,data={
            "message":"user created",
            "data":serializer.data
        })
    
class SignInUser(APIView): 

    def post(self,request) : 

        data = request.data
        serializer  = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,data={
                'error':serializer.errors
            })
        username = serializer.data['username']
        password = serializer.data['password']
        user_obj = authenticate(username=username,password=password)
         
        if user_obj is None: 
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                      "error":"Invalid credentials",
                }
            )

        token, created = Token.objects.get_or_create(user=user_obj)
        serializedUser = UserSerializers(user_obj)
        return Response(
            status=status.HTTP_200_OK,
            data={
                'user' : serializedUser.data,
                'token':token.key
            }
        )

class PostNote(APIView) : 
    
    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def post(self,request) : 
        data = request.data
        serializer = NoteSerializer(data=data)
        if not serializer.is_valid() : 
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "error" : serializer.errors,
                }
            )
        title = serializer.data['title']
        description = serializer.data['description']
        
        new_note = Note.objects.create(
            title = title,
            description = description,
            author = request.user
        )
        new_note.save()
        serialized = NoteSerializer(new_note)
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                'data':serialized.data,
            }
        )

class GetNotes(APIView) :
    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated]
     
    def get(self,request): 
        user = request.user
        notes = Note.objects.filter( author = user) 
        
        serializer = NoteSerializer(notes,many=True)
        
        return Response(
            status=status.HTTP_200_OK,
            data=   serializer.data
        )    
        
class EditNote(APIView) : 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(self,request) : 
        
        data = request.data
        id = data.get('id')

        if id is None : 
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "error":"Id is required"
                }
            )

        try :
            note = Note.objects.get(id = id)
        except Exception as e : 
              return Response(
                status = status.HTTP_400_BAD_REQUEST,
                data = {
                "error" : e
                }
            )
          
        
        serializer = NoteSerializer(note,data=data,partial=True)
        
        if not serializer.is_valid() : 
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data = {
                    "errors" : serializer.error_messages
                }
            )
        serializer.save()
        return Response(
            status=status.HTTP_200_OK,
            data = serializer.data
        )
        
class DeleteNote(APIView) : 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def delete(self,request) : 
        
        id = request.data.get('id')
        
        if id is None : 
            return Response(
                status = status.HTTP_400_BAD_REQUEST,
                data = {
                    'error' : 'Id is required'
                }
            )
        
        try : 
            note = Note.objects.get(id = id)
        except Exception as e : 
            return Response(
                status = status.HTTP_400_BAD_REQUEST,
                data = {
                    'error' : e
                }
            )
        
        if note is None : 
            return Response(
                status=status.HTTP_400_BAD_REQUEST, 
                data = {
                    'error':'id doesnt exists'
                }
            )
        
        note.delete()
        
        return Response(
            status = status.HTTP_200_OK,
            data = {
                "message" : 'Note deleted'
            }
        )
        
        