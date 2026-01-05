from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import AuthorityDashboard, IssueComment
from user.models import CivicIssue
from .serializers import (
    AuthorityDashboardSerializer, IssueCommentSerializer,
    IssueUpdateSerializer, DashboardStatsSerializer
)
from user.serializers import CivicIssueSerializer
from user.gemini_service import GeminiService

class AuthorityDashboardViewSet(viewsets.ModelViewSet):
    """ViewSet for Authority Dashboard"""
    
    queryset = AuthorityDashboard.objects.all()
    serializer_class = AuthorityDashboardSerializer
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get comprehensive dashboard overview"""
        
        # Get all issues
        all_issues = CivicIssue.objects.all()
        
        # Calculate statistics
        total_issues = all_issues.count()
        pending_issues = all_issues.filter(status='PENDING').count()
        in_progress_issues = all_issues.filter(status='IN_PROGRESS').count()
        resolved_issues = all_issues.filter(status='RESOLVED').count()
        critical_issues = all_issues.filter(priority='CRITICAL').count()
        high_priority_issues = all_issues.filter(priority='HIGH').count()
        
        # Helper for type breakdown
        def get_types(qs):
            res = {}
            for choice in CivicIssue.ISSUE_TYPES:
                c = qs.filter(issue_type=choice[0]).count()
                if c > 0: res[choice[1]] = c
            return res

        # Recent issues (last 10)
        recent_issues = all_issues.order_by('-created_at')[:10]
        
        # Area-wise statistics
        areas = all_issues.values('area').annotate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='PENDING')),
            resolved=Count('id', filter=Q(status='RESOLVED'))
        ).order_by('-total')[:10]

        data = {
            'total_issues': total_issues,
            'pending_issues': pending_issues,
            'in_progress_issues': in_progress_issues,
            'resolved_issues': resolved_issues,
            'critical_issues': critical_issues,
            'high_priority_issues': high_priority_issues,
            'issue_types': get_types(all_issues),
            'pending_types': get_types(all_issues.filter(status='PENDING')),
            'inprogress_types': get_types(all_issues.filter(status='IN_PROGRESS')),
            'resolved_types': get_types(all_issues.filter(status='RESOLVED')),
            'recent_issues': CivicIssueSerializer(recent_issues, many=True).data,
            'areas_stats': list(areas)
        }
        
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def generate_report(self, request):
        """Generate AI-powered report for authorities"""
        
        area = request.query_params.get('area', None)
        
        if area:
            issues = CivicIssue.objects.filter(area__icontains=area)
        else:
            issues = CivicIssue.objects.all()
        
        try:
            gemini_service = GeminiService()
            report = gemini_service.generate_authority_report(issues)
            
            return Response({
                'report': report,
                'generated_at': datetime.now().isoformat(),
                'area': area or 'All Areas',
                'total_issues_analyzed': issues.count()
            })
        except Exception as e:
            return Response(
                {'error': f'Report generation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def update_all_stats(self, request):
        """Update statistics for all areas"""
        
        areas = CivicIssue.objects.values_list('area', flat=True).distinct()
        
        for area in areas:
            dashboard, created = AuthorityDashboard.objects.get_or_create(area=area)
            dashboard.update_statistics()
        
        return Response({
            'message': f'Updated statistics for {len(areas)} areas',
            'areas': list(areas)
        })

class IssueManagementViewSet(viewsets.ModelViewSet):
    """ViewSet for managing issues from authority perspective"""
    
    queryset = CivicIssue.objects.all()
    serializer_class = CivicIssueSerializer
    
    def get_queryset(self):
        """Implement filtering for the issues list"""
        queryset = CivicIssue.objects.all().order_by('-created_at')
        
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        area = self.request.query_params.get('area')
        issue_type = self.request.query_params.get('issue_type')
        
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if area:
            queryset = queryset.filter(area__icontains=area)
        if issue_type:
            queryset = queryset.filter(issue_type=issue_type)
            
        return queryset
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update issue status and details"""
        
        issue = self.get_object()
        serializer = IssueUpdateSerializer(issue, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            # If resolved, set resolved_at timestamp
            if request.data.get('status') == 'RESOLVED':
                issue.resolved_at = datetime.now()
                issue.save()
            
            return Response(CivicIssueSerializer(issue).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """Add a comment to an issue"""
        
        issue = self.get_object()
        
        comment_data = {
            'issue': issue.id,
            'comment': request.data.get('comment'),
            'commented_by': request.data.get('commented_by', 'Authority')
        }
        
        serializer = IssueCommentSerializer(data=comment_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for an issue"""
        
        issue = self.get_object()
        comments = IssueComment.objects.filter(issue=issue)
        serializer = IssueCommentSerializer(comments, many=True)
        
        return Response(serializer.data)

class IssueCommentViewSet(viewsets.ModelViewSet):
    """ViewSet for issue comments"""
    
    queryset = IssueComment.objects.all()
    serializer_class = IssueCommentSerializer

@api_view(['GET'])
def analytics_view(request):
    """Get analytics data for charts and graphs"""
    
    # Time-based analytics (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_issues = CivicIssue.objects.filter(created_at__gte=thirty_days_ago)
    
    # Daily issue count
    daily_counts = []
    for i in range(30):
        date = datetime.now() - timedelta(days=i)
        count = recent_issues.filter(
            created_at__date=date.date()
        ).count()
        daily_counts.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # Status distribution
    status_distribution = {
        'pending': CivicIssue.objects.filter(status='PENDING').count(),
        'in_progress': CivicIssue.objects.filter(status='IN_PROGRESS').count(),
        'resolved': CivicIssue.objects.filter(status='RESOLVED').count(),
        'rejected': CivicIssue.objects.filter(status='REJECTED').count(),
    }
    
    # Priority distribution
    priority_distribution = {
        'low': CivicIssue.objects.filter(priority='LOW').count(),
        'medium': CivicIssue.objects.filter(priority='MEDIUM').count(),
        'high': CivicIssue.objects.filter(priority='HIGH').count(),
        'critical': CivicIssue.objects.filter(priority='CRITICAL').count(),
    }
    
    return Response({
        'daily_counts': daily_counts,
        'status_distribution': status_distribution,
        'priority_distribution': priority_distribution,
    })
