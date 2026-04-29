from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns, set_language
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap
from blog.sitemaps import PostSitemap
from portfolio.sitemaps import ProjectSitemap
from django.views.generic import TemplateView 

# Configuración de los sitemaps
sitemaps = {
    'static': StaticViewSitemap,
    'blog': PostSitemap,
    'portfolio': ProjectSitemap,
}

# 1. RUTAS GENERALES (Sin prefijo de idioma)
urlpatterns = [
    path('axxysswebadmin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('i18n/', set_language, name='set_language'),

    # Ruta de verificación de Google (Debe estar fuera de i18n para que Google la encuentre en la raíz)
    path(
        "google19c4ca07d59e3550.html",
        TemplateView.as_view(template_name="core/google19c4ca07d59e3550.html", content_type="text/html"),
    ),
]

# 2. RUTAS MULTILINGÜES (Con prefijo /es/, /fr/, /en/)
urlpatterns += i18n_patterns(
    # Sitemap dentro de i18n para generar versiones por idioma
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('', include('core.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('page/', include('pages.urls')),
    path('contact/', include('contact.urls')),
    path('blog/', include('blog.urls')),
    # Namespace de usuarios al final
    path('', include(('users.urls', 'users'), namespace='users')), 
)

# 3. ARCHIVOS MEDIA EN DESARROLLO
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)