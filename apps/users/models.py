from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    FREELANCER = 'freelancer'
    EMPLOYER = 'employer'

    USER_TYPE_CHOICES = [
        (FREELANCER, 'Freelancer'),
        (EMPLOYER, 'Employer'),
    ]
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default=FREELANCER,
    )

    username = models.CharField(max_length=150, unique=False, null=True, blank=True, verbose_name=_("username"))
    email = models.EmailField(max_length=150, unique=True, verbose_name=_("email"))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, verbose_name=_("bio"))
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    skills = models.ManyToManyField('Skill', blank=True, verbose_name=_("skills"))
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("hourly rate"))
    rating = models.FloatField(default=0.0)
    completed_projects = models.PositiveIntegerField(default=0)
    languages = models.ManyToManyField('Language', blank=True, verbose_name=_("languages"))

    company_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("company name"))
    company_website = models.URLField(blank=True, null=True)
    posted_projects = models.PositiveIntegerField(default=0)



class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("name"))  

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("name"))  

    def __str__(self):
        return self.name
    
    
    
class Rating(models.Model):
    freelancer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="ratings")
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    rating_value = models.PositiveIntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    review = models.TextField(blank=True, null=True)

    
    def average_rating(self):
        ratings = Rating.objects.filter(freelancer=self.freelancer)
        if ratings.exists():
            return float(sum(rating.rating_value for rating in ratings) / ratings.count())
        return 0.0
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.user.profile.rating = self.average_rating()
        self.user.profile.save()

  
