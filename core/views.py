from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import requests

def get_google_reviews():
    cached = cache.get('google_reviews')
    if cached:
        return cached

    url = f"https://places.googleapis.com/v1/places/{settings.GOOGLE_PLACE_ID}"
    headers = {
        "X-Goog-Api-Key": settings.GOOGLE_PLACES_API_KEY,
        "X-Goog-FieldMask": "rating,userRatingCount,reviews",
    }
    params = {
        "languageCode": "es",
    }
    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        data = r.json()
        cache.set('google_reviews', data, timeout=3600)
        return data
    except Exception as e:
        return {}

def home(request):
    google_data = get_google_reviews()
    reviews = [r for r in google_data.get("reviews", []) if r.get("text", {}).get("text")]
    context = {
        'reviews': reviews,
        'rating': google_data.get("rating", 4.8),
        'total': google_data.get("userRatingCount", 5),
        'place_id': settings.GOOGLE_PLACE_ID,
    }
    return render(request, "core/home.html", context)

def about(request):
    return render(request, "core/about.html")

DEMOS = [
    {
        'name': 'Brûlé & Cacao',
        'type': _('Pastelería artesanal'),
        'description': _('Hero visual, vitrina de productos, formulario de encargo y footer con horario y ubicación.'),
        'url': 'https://demos.axxyss.com/brule-cacao/',
        'image': 'core/img/demos/brule-cacao.webp',
        'tags': ['Tailwind CSS', 'Formspree'],
    },

    {
        'name': 'Lumière Spa',
        'type': _('Centro de estética'),
        'description': _('Hero con imagen de fondo, servicios con precios, formulario de reserva y footer elegante.'),
        'url': 'https://demos.axxyss.com/lumiere-spa/',
        'image': 'core/img/demos/lumiere-spa.webp',
        'tags': ['Tailwind CSS', 'Formspree'],
    },
]
 
def demos(request):
    return render(request, 'core/demos.html', {'demos': DEMOS})
 