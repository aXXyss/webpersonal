from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
# View
from users import views

urlpatterns = [
    path(
        route='login',
        view=views.LoginView.as_view(),
        name='login'
    ),
    path(
        route='registro',
        view=views.SignupView.as_view(),
        name='register'
    ),
    path(
        route='logout/',
        view=views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        route='registro_completado/',
        view=TemplateView.as_view(template_name='users/registerok.html'),
        name='registerok'
    ),
    path(
        route='activar/<uuid:token>/',
        view=views.ActivateAccountView.as_view(),
        name='activate'
    ),

    path(
        route='password_reset/',
        view=auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
            email_template_name='users/password_reset_email.txt',
            subject_template_name='users/password_reset_subject.txt',
        ),
        name='password_reset'
    ),
    path(
        route='password_reset/done/',
        view=auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        route='password_reset/<uidb64>/<token>/',
        view=auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        route='password_reset/complete/',
        view=auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]