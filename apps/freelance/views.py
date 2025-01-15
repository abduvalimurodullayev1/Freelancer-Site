from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.freelance.serializers import *
from django.shortcuts import render
from rest_framework import generics
from apps.users.permissions import IsOwner
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.freelance.models import Message
from apps.freelance.serializers import  MessageGetSerializer, MessageSerializer
from django.db.models import Q
from apps.users.permissions import IsSenderOrReciever

from rest_framework.response import Response



class WorkFreelanceAdd(generics.CreateAPIView):
    serializer_class = WorkForFreelancerSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    
    
    
    

class WorkFreelanceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkForFreelancerSerializer
    permission_classes = [IsAuthenticated]
    queryset = WorkForFreelancer.objects.all()
    lookup_field = 'id'
    
    



class MessageListCreateAPIView(ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsSenderOrReciever]

    def get_queryset(self):
        return Message.objects.filter(
            Q(sender=self.request.user) |
            Q(receiver=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MessageRetrieveAPIView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageGetSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        message = self.get_object()
        serializer = self.get_serializer(message)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        message = self.get_object()
        serializer = self.get_serializer(message)
        return Response(serializer.data)


class MessageHistoryAPIView(generics.ListAPIView):
    serializer_class = MessageGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        return Message.objects.filter(
            Q(sender=self.request.user) |
            Q(receiver=self.request.user),
            group__id=group_id
        ).order_by('date')




class PortfoilioView(generics.ListCreateAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    queryset = Portfolio.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

class PortfolioDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Portfolio.objects.all()
    lookup_field = 'id'
    
    
    
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    


class CategoryRetrieveView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class WorkForFreelancerListView(generics.ListAPIView):
    queryset = WorkForFreelancer.objects.all()
    serializer_class = WorkForFreelancerSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        if category_id:
            return self.queryset.filter(category_id=category_id)
        return self.queryset

class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        if category_id:
            return self.queryset.filter(category_id=category_id)
        return self.queryset
