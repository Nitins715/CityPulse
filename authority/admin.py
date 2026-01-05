from django.contrib import admin
from .models import AuthorityDashboard, IssueComment

@admin.register(AuthorityDashboard)
class AuthorityDashboardAdmin(admin.ModelAdmin):
    list_display = [
        'area', 'total_issues', 'pending_issues', 
        'in_progress_issues', 'resolved_issues', 
        'critical_issues', 'last_updated'
    ]
    list_filter = ['last_updated']
    search_fields = ['area']
    readonly_fields = ['last_updated']
    
    actions = ['update_statistics']
    
    def update_statistics(self, request, queryset):
        for dashboard in queryset:
            dashboard.update_statistics()
        self.message_user(request, f"Updated statistics for {queryset.count()} dashboards")
    update_statistics.short_description = "Update statistics for selected dashboards"

@admin.register(IssueComment)
class IssueCommentAdmin(admin.ModelAdmin):
    list_display = ['issue', 'commented_by', 'created_at']
    list_filter = ['created_at', 'commented_by']
    search_fields = ['comment', 'issue__title']
    readonly_fields = ['created_at']
