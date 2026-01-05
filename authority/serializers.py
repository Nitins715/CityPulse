from rest_framework import serializers
from .models import AuthorityDashboard, IssueComment
from user.models import CivicIssue
from user.serializers import CivicIssueSerializer

class AuthorityDashboardSerializer(serializers.ModelSerializer):
    """Serializer for Authority Dashboard"""
    
    class Meta:
        model = AuthorityDashboard
        fields = [
            'id', 'area', 'total_issues', 'pending_issues',
            'in_progress_issues', 'resolved_issues', 'critical_issues',
            'last_updated'
        ]
        read_only_fields = ['last_updated']

class IssueCommentSerializer(serializers.ModelSerializer):
    """Serializer for Issue Comments"""
    
    class Meta:
        model = IssueComment
        fields = ['id', 'issue', 'comment', 'commented_by', 'created_at']
        read_only_fields = ['created_at']

class IssueUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating issue status by authority"""
    
    class Meta:
        model = CivicIssue
        fields = ['status', 'priority', 'authority_notes', 'assigned_to']

class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for overall dashboard statistics"""
    
    total_issues = serializers.IntegerField()
    pending_issues = serializers.IntegerField()
    in_progress_issues = serializers.IntegerField()
    resolved_issues = serializers.IntegerField()
    critical_issues = serializers.IntegerField()
    high_priority_issues = serializers.IntegerField()
    
    issue_types = serializers.DictField()
    recent_issues = CivicIssueSerializer(many=True)
    areas_stats = serializers.ListField()
