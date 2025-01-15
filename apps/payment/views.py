from apps.users.permissions import IsOwner
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView 
   
from .serializers import *



class RegisterCard(generics.CreateAPIView):
    serializer_class = UserCardSerializers
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=UserCardSerializers)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)    


class DepositView(generics.CreateAPIView):
    serializer_class = TransactionHistorySerializers
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=TransactionHistorySerializers)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    
class TransactionHistoryView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializers
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def list(self, request, *args, **kwargs):
        objects = self.get_queryset()
        serializer = self.get_serializer(objects, many=True)
        return Response(serializer.data)
    

class TransactionHistoryDetail(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializers
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_object(self):
        request_user = self.request.user
        transaction = Transaction.objects.filter(user=request_user).first()  # Agar bir nechta transaction bo'lsa, faqat birinchisini qaytaradi
        if not transaction:
            raise Response("Transaction not found for this user.")  # Foydalanuvchida transaction topilmasa, xato qaytarish
        return transaction

    
    