from modeltranslation.translator import translator, TranslationOptions
from .models import Category

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'slug')  # Traducir nombre y slug

translator.register(Category, CategoryTranslationOptions)