from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views import View
from .forms import CustomUserCreationForm

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Користувач неактивний до підтвердження email
            user.save()
            messages.success(request, 'Перевірте email для підтвердження реєстрації.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def activate(request, uid, token):
    user = get_object_or_404(User, pk=uid)
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Ваш акаунт активовано!')
        return redirect('profile')
    else:
        messages.error(request, 'Невірне або прострочене посилання активації.')
        return redirect('login')


def profile(request):
    return render(request, 'accounts/profile.html')


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'Ви успішно вийшли з акаунту.')
        return redirect('login')

    def get(self, request):
        logout(request)
        messages.success(request, 'Сеанс завершено.')
        return redirect('login')
