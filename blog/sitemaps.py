# blog/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.conf import settings
from django.utils.translation import get_language
from .models import Post

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    i18n = True

    protocol = 'http' if settings.DEBUG else 'https'

    def items(self):
        return Post.objects.filter(published_date__isnull=False).order_by('-published_date')

    def location(self, obj):
        return obj.get_sitemap_url(get_language())

    def lastmod(self, obj):
        return obj.updated