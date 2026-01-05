from rest_framework import serializers
from .models import CivicIssue
from django.contrib.auth.models import User

class CivicIssueSerializer(serializers.ModelSerializer):
    """Serializer for CivicIssue model"""
    
    class Meta:
        model = CivicIssue
        fields = [
            'id', 'title', 'description', 'issue_type',
            'latitude', 'longitude', 'address', 'area', 'city',
            'image', 'status', 'priority',
            'ai_classification', 'ai_analysis', 'ai_priority',
            'reported_by', 'reporter_name', 'reporter_phone', 'reporter_email',
            'created_at', 'updated_at', 'resolved_at',
            'authority_notes', 'assigned_to'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'ai_classification', 'ai_analysis', 'ai_priority']

class CivicIssueCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new civic issues"""
    
    # Make phone optional since we have user info
    reporter_phone = serializers.CharField(max_length=15, required=False, allow_blank=True)
    
    class Meta:
        model = CivicIssue
        fields = [
            'description', 'issue_type', 'image',
            'latitude', 'longitude', 'address', 'area', 'city',
            'reporter_phone'
        ]
    
    def create(self, validated_data):
        # The AI classification and user info will be added in the view
        return super().create(validated_data)

class CivicIssueListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing issues"""
    
    class Meta:
        model = CivicIssue
        fields = [
            'id', 'title', 'issue_type', 'status', 'priority',
            'latitude', 'longitude', 'area', 'city',
            'created_at', 'image'
        ]
