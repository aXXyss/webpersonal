from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from users.forms import SignupForm
from users.models import Profile
from django.utils.translation import get_language

class SignupView(FormView):
    template_name = 'users/register.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:registerok')

    def form_valid(self, form):
        form.save(language=get_language())
        return super().form_valid(form)

class LoginView(auth_views.LoginView):
    """Login view."""
    template_name = 'users/login.html'

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""
    template_name = 'users/logged_out.html'

class ActivateAccountView(View):
    def get(self, request, token):
        profile = get_object_or_404(Profile, activation_token=token)
        if not profile.user.is_active:
            profile.user.is_active = True
            profile.user.save()
            return render(request, 'users/account_activated.html')
        else:
            return redirect('users:login')