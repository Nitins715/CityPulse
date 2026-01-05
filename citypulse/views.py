from django.shortcuts import render

def index(request):
    """User interface for reporting issues"""
    return render(request, 'citizen/index.html')

def issues(request):
    """View all issues page"""
    return render(request, 'citizen/issues.html')

def authority(request):
    """Authority dashboard page"""
    return render(request, 'authority/authority.html')

def login_page(request):
    """Login page"""
    return render(request, 'auth/login.html')

def register_page(request):
    """Register page"""
    return render(request, 'auth/register.html')

def map_view(request):
    """Map view page"""
    return render(request, 'citizen/map.html')

def profile_page(request):
    """User profile page"""
    return render(request, 'citizen/profile.html')

from django.conf import settings

def report_page(request):
    """Report issue page"""
    return render(request, 'citizen/report.html', {'maps_api_key': settings.MAPS_API_KEY})
