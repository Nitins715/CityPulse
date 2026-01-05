from django.contrib import admin
from .models import CivicIssue

@admin.register(CivicIssue)
class CivicIssueAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'issue_type', 'area', 'status', 
        'priority', 'reporter_name', 'created_at'
    ]
    list_filter = ['status', 'issue_type', 'priority', 'area', 'created_at']
    search_fields = ['title', 'description', 'area', 'reporter_name', 'address']
    readonly_fields = ['created_at', 'updated_at', 'ai_classification', 'ai_analysis', 'ai_priority']
    
    fieldsets = (
        ('Issue Information', {
            'fields': ('title', 'description', 'issue_type', 'image')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'address', 'area', 'city')
        }),
        ('Reporter Information', {
            'fields': ('reported_by', 'reporter_name', 'reporter_phone', 'reporter_email')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'assigned_to')
        }),
        ('AI Analysis', {
            'fields': ('ai_classification', 'ai_priority', 'ai_analysis'),
            'classes': ('collapse',)
        }),
        ('Authority Response', {
            'fields': ('authority_notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at'),
            'classes': ('collapse',)
        }),
    )
