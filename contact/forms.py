from django import forms
from django_recaptcha.fields import ReCaptchaField
#from django_recaptcha.widgets import ReCaptchaV2Invisible
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.utils.translation import gettext_lazy as _  # para traducciones
from django_countries.fields import CountryField
from django.utils import timezone

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
    country = CountryField(
        blank=False,
        verbose_name=_("País")
    ).formfield(
        required=True,
        # AÑADE ESTA LÍNEA para cambiar el texto de la opción vacía
        empty_label=_("Selecciona un país"), # O el texto que prefieras, ej. _("Zona geográfica")
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
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

    # --- CAMPO HONEYPOT ---
    # Lo agregamos justo antes del captcha o al final, no importa el orden visible
    honeypot_field = forms.CharField(
        required=False,
        widget=forms.HiddenInput, # Esto lo oculta en el HTML
        label=_("Por favor, no rellenes este campo") # Para accesibilidad, aunque oculto
    )
    # --- FIN CAMPO HONEYPOT ---
    
    #captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    # --- MÉTODO CLEAN PARA EL HONEYPOT ---
    def clean_honeypot_field(self):
        honeypot_value = self.cleaned_data.get('honeypot_field')
        if honeypot_value:
            # Si el honeypot tiene un valor, significa que un bot lo rellenó.
            # Lanzamos un error de validación para que el formulario no sea válido.
            # No es necesario un mensaje específico para el usuario, ya que no deberían ver este campo.
            raise forms.ValidationError("¡Bot detectado!")
        return honeypot_value # Importante devolver el valor limpio si no hay error
    # --- FIN MÉTODO CLEAN PARA EL HONEYPOT ---

    # Campo oculto para el tiempo de inicio
    start_time = forms.CharField(widget=forms.HiddenInput, required=False)


    def clean_start_time(self):
        # El tiempo en segundos desde 1970
        form_load_timestamp_str = self.cleaned_data.get('start_time')
        
        if form_load_timestamp_str:
            # Reemplazar la coma por un punto antes de la conversión
            form_load_timestamp_str = form_load_timestamp_str.replace(',', '.')
        else:
            # Si el campo está vacío, consideramos que no se registró el tiempo de carga
            # o es un bot que no lo envió. Lo tratamos como 0.
            form_load_timestamp_str = '0' 
        
        try:
            form_load_timestamp = float(form_load_timestamp_str)
        except ValueError:
            # En caso de que, por alguna razón, siga sin poder convertirse
            # Considerar esto como un intento de spam o un error.
            raise forms.ValidationError(_("Error de formato de tiempo. Posible spam."))
        # --- FIN MODIFICACIÓN ---
        
        current_timestamp = timezone.now().timestamp()
        
        # Define un tiempo mínimo aceptable (e.g., 3 segundos)
        MIN_SUBMISSION_TIME = 3 

        if form_load_timestamp == 0: # Si no se registró el tiempo de carga (posible bot o error)
            raise forms.ValidationError(_("Error de validación de tiempo."))
        
        if (current_timestamp - form_load_timestamp) < MIN_SUBMISSION_TIME:
            raise forms.ValidationError(_("Formulario enviado demasiado rápido (posible spam)."))
            
        return form_load_timestamp
    