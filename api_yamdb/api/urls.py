from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from .views import (TitleViewSet, CategoryViewSet, GenreViewSet)


router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('v1/', include(router.urls),),
]
