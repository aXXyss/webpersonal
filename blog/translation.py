from modeltranslation.translator import translator, TranslationOptions
from .models import Post

class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'slug')

translator.register(Post, PostTranslationOptions)