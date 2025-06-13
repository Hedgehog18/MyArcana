from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, activate, profile, LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/<uid>/<token>/', activate, name='activate'),
    path('profile/', profile, name='profile'),
]
