from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, activate, profile, LogoutView
from .views import CustomLoginView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('profile/', profile, name='profile'),
]
