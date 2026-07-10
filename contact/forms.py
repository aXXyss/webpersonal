from django import forms
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from .fields import TurnstileField
from django.utils import timezone


class ContactForm(forms.Form):

    # -------------------------
    # CAMPOS VISIBLES
    # -------------------------
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

    country = CountryField(
        blank_label=_("Selecciona un país"),
        verbose_name=_("País")
    ).formfield(
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
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

    # -------------------------
    # HONEYPOT (campo oculto)
    # -------------------------
    honeypot_field = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label=_("Por favor, no rellenes este campo")
    )

    # -------------------------
    # Turnstile - Cloudflare
    # -------------------------
    captcha = TurnstileField(label='')

    # -------------------------
    # CAMPO start_time (oculto)
    # -------------------------
    start_time = forms.CharField(widget=forms.HiddenInput, required=False)

    # -------------------------
    # VALIDACIONES INDIVIDUALES
    # -------------------------

    def clean_honeypot_field(self):
        """
        Si este campo oculto se rellena, casi seguro es un bot.
        """
        honeypot_value = self.cleaned_data.get('honeypot_field')
        if honeypot_value:
            raise forms.ValidationError("¡Bot detectado!")
        return honeypot_value

    def clean_start_time(self):
        """
        Valida que el formulario no se haya enviado demasiado rápido.
        (Esto se combina con una validación de tiempo en la vista).
        """
        form_load_timestamp_str = self.cleaned_data.get('start_time')

        if not form_load_timestamp_str:
            raise forms.ValidationError(_("Error de validación de tiempo."))

        # Normalizar coma → punto
        form_load_timestamp_str = form_load_timestamp_str.replace(',', '.')

        # Convertir a float
        try:
            form_load_timestamp = float(form_load_timestamp_str)
        except ValueError:
            raise forms.ValidationError(_("Error de formato de tiempo. Posible spam."))

        # Tiempo mínimo
        MIN_SUBMISSION_TIME = 3
        current_timestamp = timezone.now().timestamp()

        if (current_timestamp - form_load_timestamp) < MIN_SUBMISSION_TIME:
            raise forms.ValidationError(_("Formulario enviado demasiado rápido (posible spam)."))

        return form_load_timestamp
    
    def __init__(self, *args, remote_ip=None, **kwargs):
        super().__init__(*args, **kwargs)
        if remote_ip:
            self.fields['captcha'].remote_ip = remote_ip
