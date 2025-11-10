from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import StyleViewSet, FavoritesViewSet, search_styles


router = DefaultRouter()
router.register(r"styles", StyleViewSet)
router.register(r"favorites", FavoritesViewSet, basename='favorites')

urlpatterns = [
    path("styles/search/", search_styles, name="search_styles"),
    path("", include(router.urls)),
]

