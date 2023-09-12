from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomCreationForm
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django_registration.backends.activation.views import RegistrationView
class CustomLogoutView(auth_views.LogoutView):
    template_name = 'registration/logout.html'
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return redirect(reverse('login'))
class CustomResetPassword(auth_views.PasswordResetView):
    template_name = 'django_registration/password_reset.html'
    subject_template_name = 'django_registration/password_reset_subject.txt'
    email_template_name = 'django_registration/password_reset_email.txt'
    def get_success_url(self):
        return reverse('customResetDone')
    def get_email_options(self):
        extra_email_context = {
            "some_text": 'Любой текст для вставки в письмо'
        }
        return {
            'email_template_name': 'django_registration/password_reset_email.txt',
            'subject_template_name': 'django_registration/password_reset_subject.txt',
            'extra_email_context': extra_email_context,
            'html_email_template_name': None,
        }
class CustomResetPasswordConfirm(auth_views.PasswordResetConfirmView):
    template_name = 'django_registration/password_reset_confirm.html'
    success_url = reverse_lazy('resetIsDone')

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/register/', RegistrationView.as_view(form_class=CustomCreationForm), name='register'),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/exit/', CustomLogoutView.as_view(), name='customLogout'), #accouts/logout зарезервировано
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/pw_reset/', CustomResetPassword.as_view(), name='customReset'),
    path('accounts/pw_reset_done/', views.pw_reset_done, name='customResetDone'),
    path('accounts/pw_reset_confirm/<uidb64>/<token>/', CustomResetPasswordConfirm.as_view(), name='customResetConfirm'),
    path('accounts/pw_reset_is_done', views.reset_is_done, name='resetIsDone'),
    path('accounts/profile/', views.redirect_profile), #redirect to profile without /accounts network
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile')
]