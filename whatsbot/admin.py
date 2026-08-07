from django.contrib import admin
from .models import Conversacion, Mensaje


class MensajeInline(admin.TabularInline):
    model = Mensaje
    extra = 0
    readonly_fields = ('direccion', 'texto', 'creado')
    can_delete = False
    ordering = ('creado',)


@admin.register(Conversacion)
class ConversacionAdmin(admin.ModelAdmin):
    list_display = ('numero_cliente', 'nombre_cliente', 'creada', 'total_mensajes')
    search_fields = ('numero_cliente', 'nombre_cliente')
    ordering = ('-creada',)
    inlines = [MensajeInline]

    def total_mensajes(self, obj):
        return obj.mensajes.count()
    total_mensajes.short_description = 'Mensajes'


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('conversacion', 'direccion', 'texto_corto', 'creado')
    list_filter = ('direccion', 'creado')
    search_fields = ('texto', 'conversacion__numero_cliente', 'conversacion__nombre_cliente')
    ordering = ('-creado',)

    def texto_corto(self, obj):
        return obj.texto[:80] + ('…' if len(obj.texto) > 80 else '')
    texto_corto.short_description = 'Texto'