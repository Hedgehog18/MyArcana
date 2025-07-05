from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
import base64
from django.core.files.base import ContentFile
from django.utils import timezone

from .forms import CustomUserCreationForm
from .tokens import account_activation_token
from .models import UserProfile
from .forms import UserProfileForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Активуйте свій акаунт MyArcana.online'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            messages.success(request, 'Будь ласка, підтвердіть вашу email адресу, щоб завершити реєстрацію.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Ваш акаунт активовано. Тепер ви можете увійти.')
        return redirect('login')
    else:
        messages.error(request, 'Активація не вдалася. Посилання недійсне.')
        return redirect('register')


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Якщо прийшли дані для аватара (base64)
        cropped_data = request.POST.get('cropped_avatar_data')
        if cropped_data and cropped_data.startswith('data:image'):
            format, imgstr = cropped_data.split(';base64,')
            ext = format.split('/')[-1]

            # видаляємо старий файл
            if user_profile.avatar:
                user_profile.avatar.delete(save=False)

            file_name = f'avatar_{request.user.id}.{ext}'
            user_profile.avatar.save(file_name, ContentFile(base64.b64decode(imgstr)), save=True)
            messages.success(request, 'avatar_updated')
            return redirect('profile')

        # Якщо прийшли дані для дати
        birth_date = request.POST.get('birth_date')
        if birth_date:
            if str(user_profile.birth_date) != birth_date:
                user_profile.birth_date = birth_date
                user_profile.save()
                messages.success(request, 'birthdate_updated')
            return redirect('profile')

    form = UserProfileForm(instance=user_profile)
    registration_date = user_profile.user.date_joined
    days_since_registration = (timezone.now() - registration_date).days

    return render(request, 'accounts/profile.html', {
        'form': form,
        'registration_date': registration_date,
        'days_since_registration': days_since_registration
    })


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


class CustomLogoutView(LogoutView):
    next_page = 'login'
