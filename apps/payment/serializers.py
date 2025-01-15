from apps.payment.models import *
from rest_framework import serializers


class UserCardSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserCard
        fields = ['id', 'user', 'card_number', 'cid', 'expire_date', 'is_confirmed', 'vendor', 'status']
        read_only_fields = ['id', 'user', 'card_number', 'cid', 'expire_date', 'is_confirmed', 'vendor', 'status']

    def create(self, validated_data):
        request_user = self.context['request'].user  
        validated_data['user'] = request_user  
        return UserCard.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.card_number = validated_data.get('card_number', instance.card_number)
        instance.cid = validated_data.get('cid', instance.cid)
        instance.expire_date = validated_data.get('expire_date', instance.expire_date)
        instance.is_confirmed = validated_data.get('is_confirmed', instance.is_confirmed)
        instance.vendor = validated_data.get('vendor', instance.vendor)
        instance.status = validated_data.get('status', instance.status)
        instance.save()    
    

class TransactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'remote_id', 'status', 'paid_at', 'canceled_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'remote_id', 'status', 'paid_at', 'canceled_at', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        request_user = self.context['request'].user  
        validated_data['user'] = request_user  
        return Transaction.objects.create(**validated_data)
    

class TransactionHistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = ['id', 'transaction', 'status', 'changed_at', 'changed_by']
        read_only_fields = ['id', 'transaction', 'status', 'changed_at', 'changed_by']
        
    
    def create(self, validated_data):
        request_user = self.context['request'].user  
        validated_data['user'] = request_user  
        return TransactionHistory.objects.create(**validated_data)
    

