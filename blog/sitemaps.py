# blog/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.conf import settings
from .models import Post

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8


    def items(self):
        return Post.objects.filter(published_date__isnull=False).order_by('-published_date')


    def lastmod(self, obj):
        return obj.updated