from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.contrib.auth.models import User
from .models import CivicIssue
from .serializers import CivicIssueSerializer, CivicIssueCreateSerializer, CivicIssueListSerializer
from .gemini_service import GeminiService

class CivicIssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing civic issues
    """
    queryset = CivicIssue.objects.all()
    
    def get_queryset(self):
        """Filter queryset to only show user's own issues if not staff"""
        user = self.request.user
        if not user.is_authenticated:
            return CivicIssue.objects.none()
            
        if user.is_staff:
            queryset = CivicIssue.objects.all()
        else:
            queryset = CivicIssue.objects.filter(reported_by=user)
            
        # Add filtering by status and area
        status_filter = self.request.query_params.get('status')
        area_filter = self.request.query_params.get('area')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter.upper())
        if area_filter:
            queryset = queryset.filter(area__icontains=area_filter)
            
        return queryset.order_by('-created_at')

    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CivicIssueCreateSerializer
        elif self.action == 'list':
            return CivicIssueListSerializer
        return CivicIssueSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new civic issue with AI classification"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Use the authenticated user
        user = request.user
        
        # Get issue type to generate title
        issue_type = serializer.validated_data.get('issue_type', 'POTHOLE')
        issue_type_display = dict(CivicIssue.ISSUE_TYPES).get(issue_type, 'Issue')
        area = serializer.validated_data.get('area', 'Unknown Area')
        
        # Generate title from issue type and area
        title = f"{issue_type_display} reported in {area}"
        
        # Get phone from request or use authenticated user info
        reporter_phone = serializer.validated_data.get('reporter_phone')
        if not reporter_phone:
            # Fallback to user's phone if available, or just use username truncated to 15
            reporter_phone = (user.username)[:15]
        
        # Create the issue
        issue = serializer.save(
            reported_by=user,
            reporter_name=f"{user.first_name} {user.last_name}".strip() or user.username,
            reporter_email=user.email,
            reporter_phone=reporter_phone,
            title=title
        )
        
        # Use Gemini AI to classify the issue
        try:
            gemini_service = GeminiService()
            ai_result = gemini_service.classify_issue(
                title=issue.title,
                description=issue.description,
                address=issue.address
            )
            
            # Update issue with AI classification
            issue.ai_classification = ai_result['issue_type']
            issue.ai_priority = ai_result['priority']
            issue.ai_analysis = ai_result['analysis']
            
            # Set the issue type and priority based on AI if not manually set
            if not issue.issue_type or issue.issue_type == 'OTHER':
                issue.issue_type = ai_result['issue_type']
            if not issue.priority or issue.priority == 'MEDIUM':
                issue.priority = ai_result['priority']
            
            issue.save()
        except Exception as e:
            print(f"AI classification error: {str(e)}")
        
        # Return the created issue
        response_serializer = CivicIssueSerializer(issue)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def by_area(self, request):
        """Get issues filtered by area"""
        area = request.query_params.get('area', None)
        if area:
            issues = self.get_queryset().filter(area__icontains=area)
            serializer = self.get_serializer(issues, many=True)
            return Response(serializer.data)
        return Response({'error': 'Area parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Get issues filtered by status"""
        status_param = request.query_params.get('status', None)
        if status_param:
            issues = self.get_queryset().filter(status=status_param.upper())
            serializer = self.get_serializer(issues, many=True)
            return Response(serializer.data)
        return Response({'error': 'Status parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def map_data(self, request):
        """Get all issues for map display (non-paginated)"""
        # Always return all issues for the city-wide heatmap
        queryset = CivicIssue.objects.all()
        serializer = CivicIssueListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """Get issues near a specific location"""
        lat = request.query_params.get('lat', None)
        lng = request.query_params.get('lng', None)
        radius = float(request.query_params.get('radius', 5))  # Default 5km radius
        
        if lat and lng:
            # Simple bounding box filter (for more accurate distance, use GeoDjango)
            lat_delta = radius / 111  # Approximate km to degrees
            lng_delta = radius / (111 * abs(float(lat)))
            
            issues = self.get_queryset().filter(
                latitude__gte=float(lat) - lat_delta,
                latitude__lte=float(lat) + lat_delta,
                longitude__gte=float(lng) - lng_delta,
                longitude__lte=float(lng) + lng_delta
            )
            serializer = self.get_serializer(issues, many=True)
            return Response(serializer.data)
        return Response({'error': 'Latitude and longitude required'}, status=status.HTTP_400_BAD_REQUEST)
