from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from apps.common.models import BaseModel
from apps.users.models import Profile
from django.utils.translation import gettext_lazy as _
from apps.users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name



class WorkForFreelancer(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='works')
    budget = models.CharField(max_length=255, verbose_name=_("Budget"))
    deadline = models.DateField(verbose_name=_("Deadline"))
    demands_project = models.TextField(verbose_name=_("Demands Project"))
    date_posted = models.DateField(auto_now_add=True, verbose_name=_("Date Posted"))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='works', verbose_name=_("Category"))

    
        
    


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)



class Portfolio(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    image = models.ImageField(upload_to='portfolios/', verbose_name=_("Image"))
    url = models.URLField(verbose_name=_("URL"))
    
    class Meta:
        verbose_name = _("Portfolio")
        verbose_name_plural = _("Portfolios")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        
        

class Project(models.Model):
    freelancer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('in_progress', 'In Progress'), ('completed', 'Completed')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='projects', verbose_name=_("Category"))
