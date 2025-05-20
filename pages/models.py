from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify

# Create your models here.

class Page(models.Model):
    title = models.CharField(verbose_name="Título", max_length=200)
    link = models.CharField(verbose_name="Enlace", max_length=200, null=True, blank=True)
    content = CKEditor5Field(verbose_name="Contenido")
    order = models.SmallIntegerField(verbose_name="Orden", default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')


    class Meta:
        verbose_name = 'página'
        verbose_name_plural = 'páginas'
        ordering = ['order', 'title']

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title


class PageTranslation(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(max_length=5)  # Código de idioma (ej., 'es', 'en', 'fr')
    title = models.CharField(max_length=200)
    link = models.CharField(verbose_name="Enlace", max_length=200, null=True, blank=True)
    content = CKEditor5Field(verbose_name="Contenido", blank=True, null=True) 
    

    class Meta:
        unique_together = ('page', 'language')  # Asegura que no haya traducciones duplicadas para un idioma dado

    def __str__(self):
        return f'{self.page.title} ({self.language})'
    
    def save(self, *args, **kwargs):
        if not self.link:
            self.link = slugify(self.title)
        super().save(*args, **kwargs)