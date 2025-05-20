from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    description = CKEditor5Field(verbose_name="Descripción")
    image = models.ImageField(verbose_name="Imagen", upload_to = "projects")
    link = models.URLField(verbose_name="Dirección WEB", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")


    class Meta:                         # Creación de una clase para la traducción de los nombres de campos
        verbose_name = "proyecto"
        verbose_name_plural = "proyectos"
        ordering = ["-created"]         # Ordena la lista por fecha de creación inversa

    def __str__(self):                  # Devuelve el nombre del proyecto en el panel de administración
        return self.title
    

class ProjectTranslation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(max_length=5)  # Código de idioma (ej., 'es', 'en', 'fr')
    title = models.CharField(max_length=200)
    link = models.CharField(verbose_name="Dirección WEB", max_length=200, null=True, blank=True)
    description = CKEditor5Field(verbose_name="Descripción", blank=True, null=True) 
    

    class Meta:
        unique_together = ('project', 'language')  # Asegura que no haya traducciones duplicadas para un idioma dado

    def __str__(self):
        return f'{self.project.title} ({self.language})'
    
