
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from app.views import ItemViewSet,UserRegistrationViewSet
router=DefaultRouter()
router.register(r"items",ItemViewSet)
router.register(r'signup', UserRegistrationViewSet, basename='user-signup')

urlpatterns = [
    path('', include(router.urls)),
  
]
