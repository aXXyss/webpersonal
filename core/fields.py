import requests
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
import logging

logger = logging.getLogger(__name__)

TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


class TurnstileWidget(forms.Widget):

    def value_from_datadict(self, data, files, name):
        return data.get("cf-turnstile-response")

    def render(self, name, value, attrs=None, renderer=None):
        return format_html(
            '<div class="cf-turnstile" data-sitekey="{}"></div>',
            settings.TURNSTILE_SITE_KEY,
        )


class TurnstileField(forms.CharField):
    widget = TurnstileWidget
    default_error_messages = {
        "required": _("Por favor, verifica que no eres un robot."),
        "invalid": _("La verificación ha fallado, inténtalo de nuevo."),
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", True)
        self.remote_ip = kwargs.pop("remote_ip", None)
        super().__init__(*args, **kwargs)

    def validate(self, value):
        super().validate(value)
        if not value:
            return

        payload = {
            "secret": settings.TURNSTILE_SECRET_KEY,
            "response": value,
        }
        if self.remote_ip:
            payload["remoteip"] = self.remote_ip

        try:
            resp = requests.post(TURNSTILE_VERIFY_URL, data=payload, timeout=8)
            result = resp.json()
        except requests.RequestException as e:
            logger.warning(f"Turnstile: fallo de red/timeout al verificar: {e}")
            raise ValidationError(self.error_messages["invalid"], code="invalid")

        if not result.get("success"):
            logger.warning(f"Turnstile: verificación rechazada por Cloudflare. error-codes: {result.get('error-codes')}")
            raise ValidationError(self.error_messages["invalid"], code="invalid")