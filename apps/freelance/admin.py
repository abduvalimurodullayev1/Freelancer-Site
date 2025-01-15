from django.contrib import admin
from .models import Category, WorkForFreelancer, Project

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(WorkForFreelancer)
class WorkForFreelancerAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'budget', 'category')
    list_filter = ('category',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'freelancer', 'status', 'category')
    list_filter = ('status', 'category')
