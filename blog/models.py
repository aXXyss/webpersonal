from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from categories.models import Category

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE, blank=True, null=True)
    avatar = models.ImageField(upload_to='blog/avatars/', blank=True, null=True, verbose_name='Avatar')

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='autor')
    title = models.CharField(max_length=200,verbose_name='Título')
    slug = models.SlugField(unique=True)  # Para URLs amigables
    content = CKEditor5Field(verbose_name='Contenido')
    image = models.ImageField(upload_to='blog/images/', blank=True, null=True, verbose_name='imagen')
    categories = models.ManyToManyField(Category)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    published_date = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de publicación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    