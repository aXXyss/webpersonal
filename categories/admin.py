from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from categories.models import Category

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    """Category admin with translations."""
    list_display = ('id', 'name', 'slug')
    
    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug_es': ('name_es',),
            'slug_en': ('name_en',),
            'slug_fr': ('name_fr',),
        }