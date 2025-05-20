from django.contrib import admin
from .models import Page, PageTranslation

# Register your models here.

class PageAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('title', 'order')

class PageTranslationInline(admin.TabularInline):
    model = PageTranslation
    extra = 1  # Permite agregar una traducción adicional en el formulario

admin.site.register(Page, PageAdmin)
admin.site.register(PageTranslation)