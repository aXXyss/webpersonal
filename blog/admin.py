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
    
    fieldsets = (
        (None, {
            'fields': ('author', 'title_es', 'title_en', 'title_fr',
                      'slug_es', 'slug_en', 'slug_fr',
                      'meta_description_es', 'meta_description_en', 'meta_description_fr',
                      'content_es', 'content_en', 'content_fr',
                      'image', 'categories', 'published_date')
        }),
        ('Fechas', {
            'fields': ('created_date', 'updated'),
        }),
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug_es': ('title_es',),
            'slug_en': ('title_en',),
            'slug_fr': ('title_fr',),
        }
    
    filter_horizontal = ('categories',)
    
admin.site.register(Post, PostAdmin)