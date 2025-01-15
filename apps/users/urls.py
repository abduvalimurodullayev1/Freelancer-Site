from django.urls import path
from apps.users.views import *
app_name = 'users'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:pk>/', ProfileUpdateView.as_view(), name='profile-update'),
    path("Skills/", AddSkillsAPIView.as_view(), name="add-skills"),     
    path("Profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("RatingCreate/", RatingCreate.as_view(), name="rating"),
]