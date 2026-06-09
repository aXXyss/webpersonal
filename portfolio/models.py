from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse 
from django.utils.translation import get_language


class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="Slug")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Meta descripción")
    description = CKEditor5Field(verbose_name="Descripción")
    image = models.ImageField(verbose_name="Imagen", upload_to="projects")
    link = models.URLField(verbose_name="Dirección WEB", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "proyecto"
        verbose_name_plural = "proyectos"
        ordering = ["-created"]

    def get_absolute_url(self):
        # 1. Detecta el idioma del ciclo actual del sitemap (es, en, fr)
        lang = get_language()
        
        # El idioma base en tu base de datos es 'es' (va directo a self.slug)
        localized_slug = self.slug
        
        # 2. Si el sitemap va por el ciclo de inglés o francés, buscamos en su tabla aparte
        if lang != 'es':
            # Buscamos la traducción correspondiente en la relación inversa 'translations'
            translation = self.translations.filter(language=lang).first()
            if translation and translation.slug:
                localized_slug = translation.slug
            # Usamos 'project_detail' que es el nombre real que tienes en tus urlpatterns
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectTranslation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(max_length=5)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, verbose_name="Slug")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Meta descripción")
    link = models.CharField(verbose_name="Dirección WEB", max_length=200, null=True, blank=True)
    description = CKEditor5Field(verbose_name="Descripción", blank=True, null=True)

    class Meta:
        unique_together = ('project', 'language')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.project.title} ({self.language})'