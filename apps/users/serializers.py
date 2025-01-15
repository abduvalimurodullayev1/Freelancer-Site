from apps.users.models import *
from rest_framework import serializers



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username', 'user_type', 'password']
        
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials')

        attrs['user'] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_image', 'skills', 'hourly_rate', 'rating', 'completed_projects', 'languages', 'company_name', 'company_website', 'posted_projects']
        read_only_fields = ['rating', 'completed_projects', 'posted_projects']
        


class AddSkillsSerializer(serializers.Serializer):
    skills = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )

    def save(self, freelancer_profile):
        skills = self.validated_data['skills']
        for skill_name in skills:
            skill, created = Skill.objects.get_or_create(name=skill_name)
            freelancer_profile.skills.add(skill)
            
            
            


class RatingSerializer(serializers.ModelSerializer):
    freelancer_email = serializers.EmailField(read_only=True)  
    rating_value = serializers.ChoiceField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])  

    class Meta:
        model = Rating
        fields = ['freelancer', 'rating_value', 'review', 'freelancer_email']

    def validate(self, attrs):
        request_user = self.context['request'].user  
        freelancer = attrs.get('freelancer')
        
        if freelancer.user == request_user:
            raise serializers.ValidationError("Siz o'zingizni reytinglay olmaysiz!")
        if request_user.user_type == "freelancer":
            raise serializers.ValidationError("Freelancerlar reytinglay olmaysin!")
        
        return attrs

    def create(self, validated_data):
        employer = validated_data.pop('employer', None)  
        freelancer = validated_data.pop('freelancer')  

        rating = Rating.objects.create(employer=employer, freelancer=freelancer, **validated_data)
        return rating
