from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
import logging
from django.utils import timezone
from django.http import HttpResponse
import re

logger = logging.getLogger(__name__)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():

            # -----------------------------
            # EXTRACCIÓN DE DATOS
            # -----------------------------
            name = form.cleaned_data.get('name', '')
            company = form.cleaned_data.get('company', '')
            email = form.cleaned_data.get('email', '')
            content = form.cleaned_data.get('content', '')

            # -----------------------------
            # ANTIPATTERN SPAM SIMPLE EXISTENTE
            # -----------------------------
            blocked_name_pattern = 'robertdut'
            blocked_company_pattern = 'google'

            if name.lower() == blocked_name_pattern and company.lower() == blocked_company_pattern:
                logger.warning(f"INTENTO DE SPAM BLOQUEADO: {name}, {company}, {email}")
                return render(request, 'contact/success.html')

            # -----------------------------
            # ANTI-SPAM FUERTE
            # -----------------------------

            # 1. Bloqueo por URLs en el mensaje
            if re.search(r'https?://', content.lower()):
                logger.warning(f"SPAM BLOQUEADO (URL): {content[:60]}")
                return render(request, 'contact/success.html')

            # 2. Bloqueo por palabras de spam comunes
            spam_words = [
                "bonus", "casino", "spin", "free spins", "flash sale",
                "viagra", "promotion", "crypto", "gambling", "porn",
                "bet", "loan", "investment"
            ]

            if any(word in content.lower() for word in spam_words):
                logger.warning(f"SPAM BLOQUEADO (PALABRAS CLAVE): {content[:60]}")
                return render(request, 'contact/success.html')

            # 3. Email válido
            if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
                logger.warning(f"SPAM BLOQUEADO (EMAIL INVÁLIDO): {email}")
                return render(request, 'contact/success.html')

            # 4. Dominios sospechosos
            blocked_domains = [
                "mail.ru", "yopmail", "tempmail", "10minutemail",
                "dispostable", "guerrillamail", "proton.me", "protonmail"
            ]

            email_domain = email.split("@")[1].lower()

            if any(d in email_domain for d in blocked_domains):
                logger.warning(f"SPAM BLOQUEADO (DOMINIO): {email}")
                return render(request, 'contact/success.html')

            # 5. Validación de tiempo de sesión
            session_time = request.session.get('form_load_time')

            if not session_time:
                logger.warning("SPAM BLOQUEADO (SIN SESSION_TIME)")
                return render(request, 'contact/success.html')

            # Tiempo mínimo para completar el formulario
            if (timezone.now().timestamp() - session_time) < 3:
                logger.warning("SPAM BLOQUEADO (FORM MUY RÁPIDO)")
                return render(request, 'contact/success.html')

            # 6. Validación del REFERER
            referer = request.META.get('HTTP_REFERER', '').lower()

            allowed_referers = [
                "axxyss.com",     # dominio real
                "www.axxyss.com",
                "localhost",      # para desarrollo
                "127.0.0.1"
            ]

            if not any(allowed in referer for allowed in allowed_referers):
                logger.warning(f"SPAM BLOQUEADO (REFERER): {referer}")
                return render(request, 'contact/success.html')


            # Limpieza del tiempo de sesión después de usarlo
            try:
                del request.session['form_load_time']
            except KeyError:
                pass

            # -----------------------------
            # PROCESAMIENTO NORMAL
            # -----------------------------
            country_code = form.cleaned_data.get('country', '')
            country_name = country_code

            if 'country' in form.fields and country_code:
                for code, name_display in form.fields['country'].choices:
                    if code == country_code:
                        country_name = str(name_display)
                        break

            avisolegal = form.cleaned_data.get('avisolegal', False)
            publicidad = form.cleaned_data.get('publicidad', False)

            subject = f'Contact Form Submission from {name}'
            body = (
                f'Message from {name} ({email}):\n\n'
                f'Company: {company}\n\n'
                f'Country: {country_name} (Code: {country_code})\n\n'
                f'Consiente aviso legal: {"Sí" if avisolegal else "No"}\n\n'
                f'Consiente publicidad: {"Sí" if publicidad else "No"}\n\n'
                f'Message:\n{content}'
            )

            try:
                # Envío al destinatario principal
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    ['contacto@axxyss.com'],
                    fail_silently=False,
                )
                logger.info(f"Email enviado desde {email} a contacto@axxyss.com")

                # Copia al remitente
                send_mail(
                    f'Copy of Your Message to axxyss.com',
                    f'Thank you for your message! Here is a copy of what you sent:\n\n{body}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=True,
                )
                logger.info(f"Copia enviada a {email}")

                return render(request, 'contact/success.html')

            except Exception as e:
                logger.error(f"Error enviando email: {e}", exc_info=True)
                form.add_error(None, "Hubo un error al enviar tu mensaje. Por favor, inténtalo más tarde.")

        else:
            logger.warning(f"Validación fallida: {form.errors}")

    else:
        # GET request
        form = ContactForm()
        request.session['form_load_time'] = timezone.now().timestamp()
        logger.debug(f"Form loaded at: {request.session['form_load_time']}")

    return render(request, 'contact/contact.html', {
        'form': form,
        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY
    })
