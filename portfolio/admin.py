from django.contrib import admin
from .models import Project, ProjectTranslation


# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')  # Creación de una clase para extender el panel de Administración para mostrar por ejemplo las fechas 
    list_display = ('title',)

class PageTranslationInline(admin.TabularInline):
    model = ProjectTranslation
    extra = 1  # Permite agregar una traducción adicional en el formulario


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectTranslation)