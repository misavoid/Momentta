# momentta/views.py
from django.shortcuts import render
from momentta.models import ActivityLog
from datetime import datetime

# Momentta/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {'message': 'Welcome to Momentta!'})  # Renders a basic home page


def capture_activity(request):
    # Example logic for capturing an activity
    ActivityLog.objects.create(
        timestamp=datetime.now(),
        window_title="Sample Window",
        application="Sample App",
        category="Productivity",
        duration=5.0
    )
    return render(request, 'activity_captured.html', {'message': 'Activity Captured Successfully'})

def show_activities(request):
    # Retrieve all logged activities and pass them to the template
    activities = ActivityLog.objects.all()
    return render(request, 'activities_list.html', {'activities': activities})
