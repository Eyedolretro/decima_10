from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from issues.views import IssueViewSet, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

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
]
