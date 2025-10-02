from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
import logging
from django.utils import timezone # ¡Importante para el control de tiempo!

logger = logging.getLogger(__name__)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            # Si el formulario es válido, significa que todas las validaciones (incluyendo las de spam) pasaron.
            name = form.cleaned_data.get('name', '') 
            company = form.cleaned_data.get('company', '')
            email = form.cleaned_data.get('email', '')
            content = form.cleaned_data.get('content', '')
            
            
            # --- NUEVA LÓGICA DE BLOQUEO ESPECÍFICO POR CONTENIDO / REMITENTE ---
            # Define los patrones de spam a bloquear (insensible a mayúsculas/minúsculas)
            blocked_name_pattern = 'robertdut'
            blocked_company_pattern = 'google'

            # Verificar si coincide con el patrón de spam conocido
            is_specific_spam = False
            if name.lower() == blocked_name_pattern and \
               company.lower() == blocked_company_pattern:
                is_specific_spam = True

            if is_specific_spam:
                logger.warning(
                    f"INTENTO DE SPAM ESPECÍFICO BLOQUEADO: "
                    f"Nombre='{name}', Empresa='{company}', Email='{email}', Contenido='{content[:50]}...'"
                )
                # NO PROCESES EL MENSAJE. Redirige a una página de éxito genérica
                # para no dar pistas al bot de que ha sido detectado.
                return render(request, 'contact/success.html') # O la URL de tu página de éxito/gracias
            # --- FIN DE LÓGICA DE BLOQUEO ESPECÍFICO ---

            country_code = form.cleaned_data.get('country', '') 
            country_name = country_code

            # Recupera el nombre del país completo
            if 'country' in form.fields and country_code:
                for code, name_display in form.fields['country'].choices: # Renombrar 'name' a 'name_display' para evitar conflicto
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
                # Envío de correo al destinatario principal
                send_mail(
                    subject,
                    body,
                    # Aquí usas el correo de autenticación de Zoho
                    settings.DEFAULT_FROM_EMAIL,
                    ['contacto@axxyss.com'],
                    fail_silently=False,
                )
                logger.info(f"Email sent to {settings.DEFAULT_FROM_EMAIL} from {email}")

                # Envío de copia al remitente
                subject_sender = f'Copy of Your Message to axxyss.com'
                sender_body = f'Thank you for your message! Here is a copy of what you sent:\n\n' + body

                # Usa fail_silently=True para ignorar errores
                send_mail(
                    subject_sender,
                    sender_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=True, # <-- CAMBIA AQUÍ
                )
                logger.info(f"Copy email sent to {email}")

                return render(request, 'contact/success.html')
            except Exception as e:
                logger.error(f"Error sending email: {e}", exc_info=True)
                # No uses 'print' en producción, usa logger
                # print(f"Error sending email: {e}") 
                form.add_error(None, "Hubo un error al enviar tu mensaje. Por favor, inténtalo de nuevo más tarde.")
        else:
            # Si el formulario NO es válido, aquí puedes registrar los errores
            # para depuración si es necesario, pero los errores ya se adjuntan al formulario
            logger.warning(f"Contact form validation failed. Errors: {form.errors}")
            pass

    else: # GET request
        form = ContactForm()
        # **Importante:** Guardar el tiempo de carga del formulario para la validación de tiempo
        request.session['form_load_time'] = timezone.now().timestamp()
        logger.debug(f"Form loaded at: {request.session['form_load_time']}")
        pass

    # Pasamos la clave pública al contexto
    return render(request, 'contact/contact.html', {
        'form': form,
        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY
    })