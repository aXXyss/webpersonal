from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView, View, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from users.forms import SignupForm, LoginForm
from users.models import Profile
from django.utils.translation import get_language
from comments.models import Comment


class SignupView(FormView):
    template_name = 'users/register.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:registerok')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        remote_ip = self.request.META.get('HTTP_X_FORWARDED_FOR', self.request.META.get('REMOTE_ADDR'))
        if remote_ip and ',' in remote_ip:
            remote_ip = remote_ip.split(',')[0].strip()
        kwargs['remote_ip'] = remote_ip
        return kwargs

    def form_valid(self, form):
        form.save(language=get_language())
        return super().form_valid(form)
    

class LoginView(auth_views.LoginView):
    """Login view."""
    template_name = 'users/login.html'
    form_class = LoginForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        remote_ip = self.request.META.get('HTTP_X_FORWARDED_FOR', self.request.META.get('REMOTE_ADDR'))
        if remote_ip and ',' in remote_ip:
            remote_ip = remote_ip.split(',')[0].strip()
        kwargs['remote_ip'] = remote_ip
        return kwargs

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""
    template_name = 'users/logged_out.html'

    def get_next_page(self):
        lang = get_language()
        return f'/{lang}/'

class ActivateAccountView(View):
    def get(self, request, token):
        profile = get_object_or_404(Profile, activation_token=token)
        if not profile.user.is_active:
            profile.user.is_active = True
            profile.user.save()
            return render(request, 'users/account_activated.html')
        else:
            return redirect('users:login')

@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        comments = Comment.objects.filter(
            user=user, parent=None
        ).select_related('post').order_by('-created_at')
        context['comments'] = comments
        context['profile'] = Profile.objects.get(user=user)
        return context

@method_decorator(login_required, name='dispatch')
class ProfileEditView(UpdateView):
    model = Profile
    fields = ['photo']
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return Profile.objects.get(user=self.request.user)