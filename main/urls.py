from django.urls import path
from .views import dashboard
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('card-of-the-day/', views.card_of_the_day, name='card_of_the_day'),
    path('reading-history/', views.reading_history, name='reading_history'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
