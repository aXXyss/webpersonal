from modeltranslation.translator import translator, TranslationOptions
from .models import Post

class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'slug', 'meta_description')

translator.register(Post, PostTranslationOptions)