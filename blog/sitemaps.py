# blog/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.conf import settings
from .models import Post

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    i18n = True

    protocol = 'http' if settings.DEBUG else 'https'

    def items(self):
        return Post.objects.filter(published_date__isnull=False).order_by('-published_date')

    def lastmod(self, obj):
        return obj.updated  # Asegúrate de que tu modelo Post tenga un campo 'updated'

    def location(self, obj):
        return reverse('blog:post_detail', kwargs={'slug': obj.slug})