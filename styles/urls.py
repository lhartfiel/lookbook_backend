from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StyleViewSet, search_styles

router = DefaultRouter()
router.register(r"styles", StyleViewSet)

urlpatterns = [
    path("styles/search/", search_styles, name="search_styles"),
    path("", include(router.urls)),
]

