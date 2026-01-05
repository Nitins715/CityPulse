from django.db import models
from user.models import CivicIssue

class AuthorityDashboard(models.Model):
    """Model for authority dashboard statistics"""
    
    area = models.CharField(max_length=100, unique=True)
    total_issues = models.IntegerField(default=0)
    pending_issues = models.IntegerField(default=0)
    in_progress_issues = models.IntegerField(default=0)
    resolved_issues = models.IntegerField(default=0)
    critical_issues = models.IntegerField(default=0)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-total_issues']
    
    def __str__(self):
        return f"Dashboard - {self.area}"
    
    def update_statistics(self):
        """Update dashboard statistics from CivicIssue data"""
        issues = CivicIssue.objects.filter(area=self.area)
        
        self.total_issues = issues.count()
        self.pending_issues = issues.filter(status='PENDING').count()
        self.in_progress_issues = issues.filter(status='IN_PROGRESS').count()
        self.resolved_issues = issues.filter(status='RESOLVED').count()
        self.critical_issues = issues.filter(priority='CRITICAL').count()
        
        self.save()

class IssueComment(models.Model):
    """Model for authority comments on issues"""
    
    issue = models.ForeignKey(CivicIssue, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    commented_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment on {self.issue.title} by {self.commented_by}"
