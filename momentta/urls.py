# momentta/urls.py (app-level)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                     # Default home view
    path('capture-activity/', views.capture_activity, name='capture_activity'),
    path('activities/', views.show_activities, name='show_activities'),
]
