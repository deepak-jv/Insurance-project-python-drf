from django.urls import path
from .views import UserLoginView, UserProfileView, UserRegistrationView, UserDetailView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('customers/', UserProfileView.as_view(), name='profile'),
    path('customers/<int:pk>/', UserDetailView.as_view(), name='profile-detail'),
]
