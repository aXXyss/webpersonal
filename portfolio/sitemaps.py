# portfolio/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.conf import settings
from django.utils.translation import get_language
from .models import Project

class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    i18n = True  # Mapea automáticamente los idiomas

    # Forzar el protocolo según el entorno
    protocol = 'http' if settings.DEBUG else 'https'

    def items(self):
        # Retorna los objetos del modelo Project
        return Project.objects.all()

    def location(self, obj):
        return obj.get_sitemap_url(get_language())

    def lastmod(self, obj):
        return obj.updated
