import json
import anthropic
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Eres el asistente virtual de aXXyss Soluciones (axxyss.com), \
una empresa de desarrollo freelance full-stack \
especializada en Django/Python, WordPress y administración de servidores Linux.

Contexto de la empresa:
- Sede en Torrent, Valencia (España). Trabaja en remoto con clientes en España, \
Congo, Camerún y mérica del Norte.
- Especialidad destacada: software de gestión forestal a medida para clientes \
del sector de la madera en África central.
- Servicios: desarrollo web con Django, tiendas y sitios WordPress, \
administración de servidores Linux (VPS), aplicaciones de gestión a medida, \
sitios multilingües (español, inglés, francés).
- Se puede contactar por WhatsApp, por el formulario de contacto de la web, \
o por email a través de la web.
- No des precios exactos, indica que dependen del proyecto y que lo mejor \
es contactar directamente para presupuesto.

Instrucciones de estilo:
- Responde siempre en el mismo idioma en que te escriba el visitante \
(español, inglés o francés).
- Sé breve, cercano y profesional. Máximo 3-4 frases por respuesta.
- No uses emojis.
- No menciones el nombre completo del propietario de la empresa; \
si hace falta referirte a él, di simplemente "el equipo de aXXyss" o "nosotros".
- Si no sabes algo con certeza sobre un proyecto o precio concreto, \
anima a contactar por WhatsApp o el formulario, no inventes datos.
- No hables de temas ajenos a aXXyss o a la programación/desarrollo web.
"""

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

@require_POST
@csrf_protect
def chat(request):
    if not request.session.get('chat_verified'):
        return JsonResponse({'error': 'not_verified'}, status=403)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'invalid_json'}, status=400)

    user_message = (data.get('message') or '').strip()
    if not user_message or len(user_message) > 1000:
        return JsonResponse({'error': 'invalid_message'}, status=400)

    # Rate limit por sesión (20/hora)
    session_key = request.session.session_key or request.session.save() or request.session.session_key
    rate_key = f'chat_rate_{session_key}'
    count = cache.get(rate_key, 0)
    if count >= 20:
        return JsonResponse({'error': 'rate_limited'}, status=429)

    # Rate limit por IP (30/hora)
    ip = get_client_ip(request)
    ip_rate_key = f'chat_rate_ip_{ip}'
    ip_count = cache.get(ip_rate_key, 0)
    if ip_count >= 30:
        return JsonResponse({'error': 'rate_limited'}, status=429)

    cache.set(rate_key, count + 1, timeout=3600)
    cache.set(ip_rate_key, ip_count + 1, timeout=3600)

    # Historial de conversación guardado en sesión (máx 6 turnos para no disparar tokens)
    history = request.session.get('chat_history', [])
    history.append({'role': 'user', 'content': user_message})
    history = history[-12:]  # 6 turnos = 12 mensajes (user+assistant)

    try:
        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=300,
            system=SYSTEM_PROMPT,
            messages=history,
        )
    except anthropic.APIError as e:
        print("ERROR ANTHROPIC:", repr(e))
        return JsonResponse({'error': 'ai_unavailable', 'detail': str(e)}, status=503)

    assistant_reply = ''.join(
        block.text for block in response.content if block.type == 'text'
    )

    history.append({'role': 'assistant', 'content': assistant_reply})
    request.session['chat_history'] = history

    return JsonResponse({'reply': assistant_reply})


@require_POST
def verify_turnstile(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'invalid_json'}, status=400)

    token = data.get('token', '')
    if not token:
        return JsonResponse({'verified': False}, status=400)

    import requests
    result = requests.post(
        'https://challenges.cloudflare.com/turnstile/v0/siteverify',
        data={
            'secret': settings.TURNSTILE_SECRET_KEY,
            'response': token,
            'remoteip': request.META.get('REMOTE_ADDR'),
        },
        timeout=5,
    ).json()

    if result.get('success'):
        request.session['chat_verified'] = True
        return JsonResponse({'verified': True})

    return JsonResponse({'verified': False}, status=403)
