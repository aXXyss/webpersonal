# portfolio/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.conf import settings
from .models import Project

class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7


    def items(self):
        # Retorna los objetos del modelo Project
        return Project.objects.all()


    def lastmod(self, obj):
        return obj.updated
