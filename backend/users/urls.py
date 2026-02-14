from django.urls import path
from .views import RegisterView, UserDetailView, PublicUserProfileView, ProfileUpdateView, TalentListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/me/', UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/', PublicUserProfileView.as_view(), name='public_user_profile'),
    path('users/profile/', ProfileUpdateView.as_view(), name='profile_update'),
    path('users/', TalentListView.as_view(), name='talent_list'),
]
