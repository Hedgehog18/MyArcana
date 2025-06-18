from django.urls import path
from .views import register, activate, profile, CustomLogoutView
from .views import CustomLoginView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('profile/', profile, name='profile'),
]
