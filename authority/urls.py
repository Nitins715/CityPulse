from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthorityDashboardViewSet, IssueManagementViewSet,
    IssueCommentViewSet, analytics_view
)

router = DefaultRouter()
router.register(r'dashboard', AuthorityDashboardViewSet, basename='authority-dashboard')
router.register(r'issues', IssueManagementViewSet, basename='authority-issues')
router.register(r'comments', IssueCommentViewSet, basename='issue-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', analytics_view, name='analytics'),
]
