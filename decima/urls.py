from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from issues.views import (
    UserViewSet,
    ProjetViewSet,
    IssueViewSet,
    CommentViewSet,
    ProjetCommentViewSet,
    ProjetCollaborateurViewSet,
    RegisterView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# -----------------------
# Routers principaux
# -----------------------
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projets', ProjetViewSet, basename='projet')

# Router imbriqué pour projets
projets_router = nested_routers.NestedDefaultRouter(router, r'projets', lookup='projet')
projets_router.register(r'issues', IssueViewSet, basename='projet-issues')
projets_router.register(r'comments', ProjetCommentViewSet, basename='projet-comments')
projets_router.register(r'collaborateurs', ProjetCollaborateurViewSet, basename='projet-collaborateurs')

# Router imbriqué pour comments dans issues
issues_router = nested_routers.NestedDefaultRouter(projets_router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewSet, basename='issue-comments')

# -----------------------
# Swagger / Redoc
# -----------------------


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Swagger UI pour mon projet",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

# Définit l'auth JWT pour Swagger
swagger_schema = schema_view.with_ui('swagger', cache_timeout=0)

# -----------------------
# URL Patterns
# -----------------------
urlpatterns = [
    path('admin/', admin.site.urls),

    # OpenAPI Schema et Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # API principale
    path('api/', include('issue_tracker.urls')),
]