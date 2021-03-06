from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PostViewSet

router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet, basename='post')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
