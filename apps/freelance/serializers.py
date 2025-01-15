from apps.freelance.models import *
from rest_framework import serializers


class WorkForFreelancerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkForFreelancer
        fields = ['title', 'description', 'budget', 'deadline', 'demands_project', 'user']
        read_only_fields = ['date_posted', 'user']  

    def create(self, validated_data):
        request_user = self.context['request'].user  
        validated_data['user'] = request_user  
        return WorkForFreelancer.objects.create(**validated_data)



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ()


class MessageGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ['sender', 'receiver', 'content']
        


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['title', 'description', 'image', 'url']
        read_only_fields = ['user']
        
    def create(self, validated_data):
        request_user = self.context['request'].user
        validated_data['user'] = request_user  
        return Portfolio.objects.create(**validated_data)



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']
        read_only_fields = ['user']
        
    
    

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project 
        fields = ['title', 'description', 'freelancer', ]
        read_only_fields = ['freelancer', 'status']