from django.urls import path
from apps.freelance.views import *
app_name = "freelance"

urlpatterns = [
    path("work/<int:pk>/", WorkFreelanceDetail.as_view(), name="work-detail"),
    path("work/add/", WorkFreelanceAdd.as_view(), name="work-add"),
    path("messages/", MessageListCreateAPIView.as_view(), name="message-list-create"),
    path("messages/<int:pk>/", MessageRetrieveAPIView.as_view(), name="message-retrieve"),
    path("portfoilio/", PortfoilioView.as_view(), name="portfoilio"),   
    path("portfoilio/<int:id>/", PortfolioDetail.as_view(), name="portfoilio-detail"),
    path("category/", CategoryListView.as_view(), name="category-list"),
    path("category/<int:id>/", CategoryRetrieveView.as_view(), name="category-detail"),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('works/', WorkForFreelancerListView.as_view(), name='works'),
    path('projects/', ProjectListView.as_view(), name='projects'),
]


