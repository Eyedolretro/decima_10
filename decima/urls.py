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
    # Admin
    path('admin/', admin.site.urls),

    # Routes API principales
    path('api/', include(router.urls)),
    path('api/', include(projets_router.urls)),
    path('api/', include(issues_router.urls)),

    # Auth DRF
    path('api-auth/', include('rest_framework.urls')),

    # Auth Register
    path('api/register/', RegisterView.as_view(), name='register'),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Accueil API
    path('', lambda request: HttpResponse("Bienvenue sur l'API!"), name='home'),

    # Swagger / Redoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
