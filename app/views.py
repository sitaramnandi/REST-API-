
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from app.models import Item
from app.serializers import ItemSerializer, UserRegistrationSerializer
import logging


# Set up logging
logger = logging.getLogger("app.views")

# Viewset for managing inventory items
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]  # All operations require authentication


    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def popular(self, request):
        """
        Handle fetching popular items (with quantity >= 100).
        Results are cached for 300 seconds.
        """
        logger.info("Fetching popular items.")
        cached_items = cache.get("popular_items")

        if cached_items:
            logger.info("Returning cached popular items.")
            return Response(cached_items)
        else:
            logger.info("Cache miss; fetching from database.")

        try:
            popular_items = Item.objects.filter(quantity__gte=100)
            serializer = ItemSerializer(popular_items, many=True)
            cache.set("popular_items", serializer.data, timeout=300)
            logger.info("Cached popular items for future requests.")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching popular items: {str(e)}")
            return Response({"error": "Failed to fetch popular items."}, status=500)

# Viewset for user registration
class UserRegistrationViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]  # Allow all users to register

    def create(self, request):
        """
        Handle user registration.
        """
        logger.info("Registering a new user.")
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User {user.username} registered successfully.")

            # Create JWT tokens
            refresh = RefreshToken.for_user(user)

            # Return user data along with tokens
            return Response({
                'username': user.username,
                'email': user.email,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)
        
        logger.error("User registration failed.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
