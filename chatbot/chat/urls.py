from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ChatGroupViewSet, MessageViewSet, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Create a router for DRF ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'groups', ChatGroupViewSet, basename='group')
router.register(r'messages', MessageViewSet, basename='message')
# router.register(r'login', TokenObtainPairView, basename='login')

urlpatterns = [
    path('', include(router.urls)),  # Include DRF-generated routes
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout')
]
