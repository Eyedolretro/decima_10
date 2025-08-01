from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from issues.views import IssueViewSet, CommentViewSet, RegisterView, ProjetViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'issues', IssueViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'projets', ProjetViewSet, basename='projet')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/register/', RegisterView.as_view(), name='register'),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
