import hashlib
import hmac
import json
import logging

import anthropic
import requests
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from helpdesk.views import client, SYSTEM_PROMPT
from django.core.cache import cache

from .models import Conversacion, Mensaje

logger = logging.getLogger(__name__)

GRAPH_API_URL = f"https://graph.facebook.com/v21.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"


@csrf_exempt
def webhook(request):
    if request.method == 'GET':
        return verificar_webhook(request)
    elif request.method == 'POST':
        return recibir_mensaje(request)
    return HttpResponseForbidden()


def verificar_webhook(request):
    """Meta llama a esto UNA VEZ al configurar el webhook en el panel."""
    modo = request.GET.get('hub.mode')
    token = request.GET.get('hub.verify_token')
    challenge = request.GET.get('hub.challenge')

    if modo == 'subscribe' and token == settings.WHATSAPP_VERIFY_TOKEN:
        return HttpResponse(challenge)
    return HttpResponseForbidden('Verificación fallida')


def validar_firma(request):
    """Comprueba que el POST viene realmente de Meta."""
    firma = request.headers.get('X-Hub-Signature-256', '')
    if not firma.startswith('sha256='):
        return False
    firma = firma[len('sha256='):]
    esperada = hmac.new(
        settings.WHATSAPP_APP_SECRET.encode(),
        request.body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(firma, esperada)


def recibir_mensaje(request):
    if not validar_firma(request):
        logger.warning("Firma de webhook inválida")
        return HttpResponseForbidden()

    data = json.loads(request.body)
    logger.info("Webhook recibido: %s", data)

    try:
        entry = data['entry'][0]
        cambio = entry['changes'][0]['value']

        # Ignoramos notificaciones de "estado" (entregado, leído, etc.)
        if 'messages' not in cambio:
            return JsonResponse({'status': 'ignored'})

        mensaje_meta = cambio['messages'][0]
        mensaje_id = mensaje_meta.get('id')

        # Deduplicación: Meta reintenta el webhook si no recibe 200 a tiempo,
        # lo que puede generar respuestas duplicadas para el mismo mensaje.
        if mensaje_id:
            dedup_key = f'whatsbot_msg_{mensaje_id}'
            if cache.get(dedup_key):
                logger.info("Mensaje duplicado ignorado: %s", mensaje_id)
                return JsonResponse({'status': 'duplicate'})
            cache.set(dedup_key, True, timeout=3600)

        numero = mensaje_meta['from']
        texto_entrante = mensaje_meta.get('text', {}).get('body', '')

        nombre = cambio.get('contacts', [{}])[0].get('profile', {}).get('name', '')

        conversacion, _ = Conversacion.objects.get_or_create(
            numero_cliente=numero,
            defaults={'nombre_cliente': nombre}
        )
        Mensaje.objects.create(conversacion=conversacion, direccion=Mensaje.ENTRANTE, texto=texto_entrante)

        respuesta = generar_respuesta(conversacion, texto_entrante)

        Mensaje.objects.create(conversacion=conversacion, direccion=Mensaje.SALIENTE, texto=respuesta)
        enviar_mensaje_whatsapp(numero, respuesta)

    except (KeyError, IndexError) as e:
        logger.warning("Estructura de webhook inesperada: %s", e)

    return JsonResponse({'status': 'ok'})


def enviar_mensaje_whatsapp(numero, texto):
    headers = {
        'Authorization': f'Bearer {settings.WHATSAPP_ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }
    payload = {
        'messaging_product': 'whatsapp',
        'to': numero,
        'type': 'text',
        'text': {'body': texto},
    }
    r = requests.post(GRAPH_API_URL, headers=headers, json=payload, timeout=10)
    if not r.ok:
        logger.error("Error enviando WhatsApp: %s - %s", r.status_code, r.text)
    return r


def generar_respuesta(conversacion, texto_entrante):
    # Rate limit por número de WhatsApp (20/hora, mismo criterio que el chat web)
    rate_key = f'whatsbot_rate_{conversacion.numero_cliente}'
    count = cache.get(rate_key, 0)
    if count >= 20:
        return "Has alcanzado el límite de mensajes por hora. Por favor, inténtalo más tarde o contacta por email."
    cache.set(rate_key, count + 1, timeout=3600)

    historial = conversacion.mensajes.order_by('-creado')[:12][::-1]
    mensajes = [
        {'role': 'user' if m.direccion == Mensaje.ENTRANTE else 'assistant', 'content': m.texto}
        for m in historial
    ]
    mensajes.append({'role': 'user', 'content': texto_entrante})

    try:
        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=300,
            system=SYSTEM_PROMPT,
            messages=mensajes,
        )
    except anthropic.APIError as e:
        logger.error("Error Anthropic en whatsbot: %s", repr(e))
        return "Disculpa, en este momento no puedo responder. Contacta por email o vuelve a intentarlo en unos minutos."

    return ''.join(block.text for block in response.content if block.type == 'text')