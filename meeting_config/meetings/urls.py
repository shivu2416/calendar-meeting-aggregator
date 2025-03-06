from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CalendarMeetingViewSet

router = DefaultRouter()
router.register(r'meetings', CalendarMeetingViewSet, basename='meetings')

urlpatterns = [
    path('api/', include(router.urls)),  # This automatically maps ViewSet actions
]