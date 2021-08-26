from django.conf.urls import include
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from api.views import subscription_view


urlpatterns = [
    path('users/subscriptions/', subscription_view, name='all_subsriptors'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
