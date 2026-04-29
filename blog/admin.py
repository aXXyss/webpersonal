from django.contrib import admin
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget
from modeltranslation.admin import TranslationAdmin
from .models import Post, UserProfile

admin.site.register(UserProfile)

class PostAdmin(TranslationAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget()},
    }
    
    readonly_fields = ('created_date', 'updated')
    list_display = ('title', 'author', 'published_date', 'created_date')
    list_filter = ('created_date', 'updated', 'published_date')

    # Slug traducido se genera desde title traducido
    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug_es': ('title_es',),
            'slug_en': ('title_en',),
            'slug_fr': ('title_fr',),
        }
    
    filter_horizontal = ('categories',)
    
admin.site.register(Post, PostAdmin)