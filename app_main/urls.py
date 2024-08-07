"""
App Profile URLs
"""
from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from .views import ProfileView

profile_router = routers.DefaultRouter()
profile_router.register('profile', ProfileView)

urlpatterns = [
    path('', include(profile_router.urls)),
]