from django.db import models
from django.contrib.auth.models import User

class CivicIssue(models.Model):
    """Model for civic issues reported by users"""
    
    ISSUE_TYPES = [
        ('POTHOLE', 'Potholes'),
        ('GARBAGE', 'Garbage overflow'),
        ('WATER', 'Water leakage'),
        ('STREETLIGHT', 'Broken streetlights'),
        ('ROAD_OBSTRUCTION', 'Road obstruction'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('REJECTED', 'Rejected'),
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField()
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPES, default='OTHER')
    
    # Location Information
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=500)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default='Unknown')
    
    # Media
    image = models.ImageField(upload_to='issues/', null=True, blank=True)
    image_labels = models.TextField(null=True, blank=True, help_text="AI-detected labels for the uploaded image")
    
    # Status and Priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    
    # AI Generated Fields
    ai_classification = models.CharField(max_length=20, choices=ISSUE_TYPES, null=True, blank=True)
    ai_analysis = models.TextField(null=True, blank=True)
    ai_priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, null=True, blank=True)
    
    # User Information
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_issues')
    reporter_name = models.CharField(max_length=100)
    reporter_phone = models.CharField(max_length=15)
    reporter_email = models.EmailField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Authority Response
    authority_notes = models.TextField(null=True, blank=True)
    assigned_to = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['issue_type', 'area']),
            models.Index(fields=['latitude', 'longitude']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.area} ({self.status})"
