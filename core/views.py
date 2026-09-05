from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import requests
from .models import Resena, ResenasConfig


def home(request):
    reviews = Resena.objects.all()
    config = ResenasConfig.get_config()
    context = {
        'reviews': reviews,
        'rating': config.rating,
        'total': config.total,
        'place_id': settings.GOOGLE_PLACE_ID,
    }
    return render(request, "core/home.html", context)



def about(request):
    return render(request, "core/about.html")

DEMOS = [

    {
        'name': 'AquaFix',
        'type': _('Fontanería'),
        'description': _('Hero con contacto de urgencias, 6 servicios, proceso paso a paso y dos formularios: consulta rápida y presupuesto detallado.'),
        'url': 'https://demos.axxyss.com/aquafix/',
        'image': 'core/img/demos/aquafix.webp',
        'tags': ['CSS puro', 'Formspree'],
    },

    {
        'name': 'Brûlé & Cacao',
        'type': _('Pastelería artesanal'),
        'description': _('Hero visual, vitrina de productos, formulario de encargo y footer con horario y ubicación.'),
        'url': 'https://demos.axxyss.com/brule-cacao/',
        'image': 'core/img/demos/brule-cacao.webp',
        'tags': ['Tailwind CSS', 'Formspree'],
    },

    {
        'name': 'Old Town Barber',
        'type': _('Barbería'),
        'description': _('Hero con imagen, servicios con precios, equipo de barberos, integración Booksy y formulario de contacto.'),
        'url': 'https://demos.axxyss.com/oldtown-barber/',
        'image': 'core/img/demos/oldtown-barber.webp',
        'tags': ['CSS puro', 'Booksy', 'Formspree'],
    },

    {
        'name': 'Lumière Spa',
        'type': _('Centro de estética'),
        'description': _('Hero con imagen de fondo, servicios con precios, formulario de reserva y footer elegante.'),
        'url': 'https://demos.axxyss.com/lumiere-spa/',
        'image': 'core/img/demos/lumiere-spa.webp',
        'tags': ['Tailwind CSS', 'Formspree'],
    },

    {
        'name': 'FORGE Training',
        'type': _('Entrenador personal'),
        'description': _('Hero impactante, programas con precios, sección entrenador y formulario de contacto.'),
        'url': 'https://demos.axxyss.com/forge-training/',
        'image': 'core/img/demos/forge-training.webp',
        'tags': ['Tailwind CSS', 'Formspree'],
    },
]

def servicios(request):
    return render(request, "core/servicios.html")

def infraestructura(request):
    return render(request, "core/infraestructura.html")


def fuelaxflow(request):
    return render(request, "core/fuelaxflow.html")

 
def demos(request):
    return render(request, 'core/demos.html', {'demos': DEMOS})
 