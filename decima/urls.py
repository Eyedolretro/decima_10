from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from django.http import HttpResponse
from issues.views import (
    IssueViewSet,
    CommentViewSet,
    RegisterView,
    ProjetViewSet,
    ProjetCommentViewSet,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# -----------------------
# Router principal
# -----------------------
router = routers.DefaultRouter()
router.register(r'projets', ProjetViewSet, basename='projet')
router.register(r'comments', CommentViewSet, basename='comment')

# -----------------------
# Router imbriqué : issues dans projets
# /api/projets/{projet_id}/issues/
# -----------------------
projets_router = nested_routers.NestedDefaultRouter(router, r'projets', lookup='projet')
projets_router.register(r'issues', IssueViewSet, basename='projet-issues')
projets_router.register(r'comments', ProjetCommentViewSet, basename='projet-comments')

# -----------------------
# Router imbriqué : comments dans issues
# /api/projets/{projet_id}/issues/{issue_id}/comments/
# -----------------------
issues_router = nested_routers.NestedDefaultRouter(projets_router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewSet, basename='issue-comments')

# -----------------------
# URL Patterns
# -----------------------
urlpatterns = [
    path('admin/', admin.site.urls),

    # Routes API principales
    path('api/', include(router.urls)),
    path('api/', include(projets_router.urls)),
    path('api/', include(issues_router.urls)),

    # Auth DRF
    path('api-auth/', include('rest_framework.urls')),
    path('api/register/', RegisterView.as_view(), name='register'),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Accueil API
    path('', lambda request: HttpResponse("Bienvenue sur l'API!"), name='home'),
]
