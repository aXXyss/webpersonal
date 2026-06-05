from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from users.models import Profile
from django.urls import reverse

class SignupForm(forms.Form):
    """Sign up form."""
    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput()
    )
    username = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.TextInput()
    )
    password = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput()
    )
    password_confirmation = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput()
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con este email.')
        return email

    def clean(self):
        data = super().clean()
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return data

    def save(self):
        data = self.cleaned_data
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        user.is_active = False
        user.save()
        profile = Profile(user=user)
        profile.save()

        try:

            activation_url = f"{settings.SITE_URL}{reverse('users:activate', kwargs={'token': profile.activation_token})}"
            send_mail(
                subject='Activa tu cuenta en aXXyss Soluciones',
                message=f"""Hola {user.username},

Gracias por registrarte en aXXyss Soluciones.

Para activar tu cuenta haz clic en el siguiente enlace:

{activation_url}

Si no te has registrado, ignora este mensaje.

Un saludo,
Joaquin Denis
aXXyss Soluciones
https://axxyss.com
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error enviando email de activación: {e}")