from django.contrib.sitemaps import Sitemap
from django.conf import settings
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return [
            'home',
            'about',
            'contact:contact',
            'demos',
            'servicios',
            'infraestructura',
            'fuelaxflow',
            'blog:post_list',
            'portfolio:project_list',
        ]
      

    def location(self, item):
        return reverse(item)