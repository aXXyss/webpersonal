from django.contrib import admin

from .models import Resena

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('autor', 'rating', 'orden')