# portfolio/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Project

class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return reverse('portfolio:project_detail', kwargs={'project_id': obj.id})
