from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from users.models import Profile
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import activate, get_language

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
            raise forms.ValidationError(_('Este nombre de usuario ya está en uso.'))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Ya existe una cuenta con este email.'))
        return email

    def clean(self):
        data = super().clean()
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError(_('Las contraseñas no coinciden.'))
        return data

    def save(self, language='es'):
        data = self.cleaned_data
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        user.is_active = False
        user.save()
        profile = Profile(user=user)
        profile.save()

        current_language = get_language()
        activate(language)

        try:
            activation_url = f"{settings.SITE_URL}/{language}/activar/{profile.activation_token}/"
            msg_template = str(_('Hola %(username)s,\n\nGracias por registrarte en aXXyss Soluciones.\n\nPara activar tu cuenta haz clic en el siguiente enlace:\n\n%(url)s\n\nSi no te has registrado, ignora este mensaje.\n\nUn saludo,\nJoaquin Denis\naXXyss Soluciones\nhttps://axxyss.com\n'))
            message = msg_template.replace('\\n', '\n') % {'username': user.username, 'url': activation_url}

            send_mail(
                subject=str(_('Activa tu cuenta en aXXyss Soluciones')),
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error enviando email de activación: {e}")
        finally:
            activate(current_language)