from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns, set_language
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap
from blog.sitemaps import PostSitemap
from portfolio.sitemaps import ProjectSitemap
# Importa TemplateView para servir el archivo
from django.views.generic import TemplateView 



sitemaps = {
    'static': StaticViewSitemap,
    'blog': PostSitemap,
    'portfolio': ProjectSitemap,
}

urlpatterns = [
    path('axxysswebadmin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('i18n/', set_language, name='set_language'), # Agrega esta línea

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # --- RUTA DE VERIFICACIÓN DE GOOGLE (FUERA DE i18n_patterns) ---
    path(
        "google19c4ca07d59e3550.html",
        TemplateView.as_view(template_name="core/google19c4ca07d59e3550.html", content_type="text/html"),
    ),
]
urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('page/', include('pages.urls')),
    path('contact/', include('contact.urls')),
    path('blog/', include('blog.urls')),
    path('', include(('users.urls', 'users'), namespace='users')), # Colocar al final, para evitar conflictos con otras rutas
    path('comments/', include('comments.urls')),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)