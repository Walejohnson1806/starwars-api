from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import FilmViewSet, CommentViewSet

# Main router
router = DefaultRouter()
router.register(r'films', FilmViewSet, basename='film')

# Nested router for comments under films
films_router = routers.NestedDefaultRouter(router, r'films', lookup='film')
films_router.register(r'comments', CommentViewSet, basename='film-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(films_router.urls)),
]