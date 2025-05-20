from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible
from django.utils.translation import gettext_lazy as _  # para traducciones

class ContactForm(forms.Form):
    name = forms.CharField(
        label=_("Nombre"),
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _("Nombre y Apellidos")
        }),
        min_length=3,
        max_length=100
    )
    company = forms.CharField(
        label=_("Empresa"),
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _("Empresa")
        }),
        min_length=3,
        max_length=100
    )
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _("Correo electrónico")
        }),
        min_length=3,
        max_length=100
    )
    zone = forms.CharField(
        label=_("Zona geográfica"),
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _("Zona geográfica")
        }),
        min_length=3,
        max_length=100
    )
    content = forms.CharField(
        label=_("Contenido"),
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': _("Mensaje")
        }),
        min_length=10,
        max_length=1000
    )
    avisolegal = forms.BooleanField(
        required=True,
        label=_("Aviso Legal"),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    publicidad = forms.BooleanField(
        required=False,
        label=_("Publicidad"),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
