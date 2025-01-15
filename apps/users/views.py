from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.users.serializers import *
from apps.users.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from apps.users.permissions import IsOwner
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics



class RegisterView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class LoginView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']  
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)  
            if user:
                return Response({'token': user.token()}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    

class ProfileUpdateView(generics.UpdateAPIView):
    permission_classes = [IsOwner]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)    
    
class AddSkillsAPIView(APIView):
    @swagger_auto_schema(request_body=AddSkillsSerializer)
    def post(self, request, *args, **kwargs):
        freelancer_profile = get_object_or_404(Profile, user=request.user)
        serializer = AddSkillsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(freelancer_profile)
        return Response({"message": "Skills added successfully!"})


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = 'pk'
    


class RatingCreate(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user  
        serializer.save(employer=request_user)  