from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import CustomUser
from .forms import UserRegistrationForm, UserProfileForm

class RegisterView(CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        # messages.success(self.request, 'Регистрация прошла успешно! Теперь вы можете войти.')
        # return redirect(self.success_url)

        # ОТПРАВКА ПРИВЕТСТВЕННОГО ПИСЬМА
        try:
            send_mail(
                subject='Добро пожаловать в наш сервис!',
                message=self._get_welcome_email_text(user),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            messages.success(
                self.request,
                f'Регистрация прошла успешно! На почту {user.email} отправлено приветственное письмо.'
            )
        except Exception as e:
            # Если отправка не удалась, все равно сообщаем об успешной регистрации
            messages.success(
                self.request,
                f'Регистрация прошла успешно! Приветственное письмо не отправлено (ошибка: {str(e)})'
            )

        return redirect(self.success_url)

    def _get_welcome_email_text(self, user):
        """Текстовая версия приветственного письма"""
        name = user.first_name or user.email.split('@')[0]
        return f"""
Уважаемый(ая) {name}!

Добро пожаловать в наш сервис!

Ваш email для входа: {user.email}

Спасибо, что выбрали наш сервис. Мы рады приветствовать вас!

С уважением,
Команда сервиса
"""

class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)
