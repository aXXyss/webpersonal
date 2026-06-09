from django.contrib.sitemaps import Sitemap
from django.conf import settings
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    i18n = True

    protocol = 'http' if settings.DEBUG else 'https'

    def items(self):
        return ['home', 'about', 'contact:contact']
      

    def location(self, item):
        return reverse(item)