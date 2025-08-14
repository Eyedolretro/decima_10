from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from issues.views import IssueViewSet, RegisterView
from django.http import HttpResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from issues.views import test_postman
from .views import test_postman, test_postman_post




router = routers.DefaultRouter()
router.register(r'issues', IssueViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API CRUD tickets
    path('api/', include(router.urls)),

    # Authentification
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', test_postman, name='test_postman'),
    path('test-post/', test_postman_post, name='test_postman_post'),
]
