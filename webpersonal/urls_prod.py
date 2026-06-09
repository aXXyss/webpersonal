from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns, set_language
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap
from blog.sitemaps import PostSitemap
from portfolio.sitemaps import ProjectSitemap
from django.views.generic import TemplateView, RedirectView

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

     path(
        '34a9356adbb141a18b3c397a432e0b4c.txt',
        TemplateView.as_view(
            template_name='core/34a9356adbb141a18b3c397a432e0b4c.txt',
            content_type='text/plain'
        ),
    ),

     # --- REDIRECCIONES 301 (URLs antiguas → URLs nuevas) ---
     # Posts Django/Debian (slugs con "-12" al final, renombrados al traducir)
     path('es/blog/post/desarrollo-web-con-django-en-debian-12/',
         RedirectView.as_view(url='/es/blog/post/desarrollo-web-con-django-en-debian/', permanent=True)),
     path('en/blog/post/desarrollo-web-con-django-en-debian-12/',
         RedirectView.as_view(url='/en/blog/post/web-development-with-django-on-debian/', permanent=True)),
     path('fr/blog/post/desarrollo-web-con-django-en-debian-12/',
         RedirectView.as_view(url='/fr/blog/post/developpement-web-avec-django-sur-debian/', permanent=True)),

     # Posts aaPanel (slugs en español en versiones EN/FR, renombrados al traducir)
     path('en/blog/post/que-es-aapanel/',
         RedirectView.as_view(url='/en/blog/post/what-is-aapanel/', permanent=True)),
     path('fr/blog/post/que-es-aapanel/',
         RedirectView.as_view(url='/fr/blog/post/quest-ce-que-aapanel/', permanent=True)),

     # Post WebP (slug en inglés en versión ES, renombrado al traducir)
     path('es/blog/post/complete-guide-how-to-convert-images-to-webp/',
         RedirectView.as_view(url='/es/blog/post/guia-completa-como-convertir-imagenes-a-webp/', permanent=True)),

     # Post Como migrar Django (slug en inglés en versión ES, renombrado al traducir
     path('es/blog/post/como-migrar-django-shared-hosting-vps-nginx-gunico/',
	     RedirectView.as_view(url='/es/blog/post/como-migrar-django-a-vps-nginx-gunicorn/', permanent=True)),
     path('en/blog/post/how-to-migrate-your-django-app-from-shared-hosting-to/',
     	RedirectView.as_view(url='/en/blog/post/how-to-migrate-django-to-vps-nginx-gunicorn/', permanent=True)),
     path('fr/blog/post/comment-migrer-votre-application-django-dun-hebergemen/',
	     RedirectView.as_view(url='/fr/blog/post/migrer-django-vers-vps-nginx-gunicorn/', permanent=True)),
         
]

# 2. RUTAS MULTILINGÜES (Con prefijo /es/, /fr/, /en/)
urlpatterns += i18n_patterns(
     path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
     path('', include('core.urls')),
     path('portfolio/', include('portfolio.urls')),
     path('page/', include('pages.urls')),
     path('contact/', include('contact.urls')),
     path('blog/', include('blog.urls')),
     path('comments/', include('comments.urls')),
     # Namespace de usuarios al final
     path('', include(('users.urls', 'users'), namespace='users')), 
)

# 3. ARCHIVOS MEDIA EN DESARROLLO
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
