from django.db import models


class Conversacion(models.Model):
    numero_cliente = models.CharField(max_length=20, db_index=True)
    nombre_cliente = models.CharField(max_length=100, blank=True)
    creada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_cliente or self.numero_cliente}"


class Mensaje(models.Model):
    ENTRANTE = 'in'
    SALIENTE = 'out'
    DIRECCION_CHOICES = [(ENTRANTE, 'Entrante'), (SALIENTE, 'Saliente')]

    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    direccion = models.CharField(max_length=3, choices=DIRECCION_CHOICES)
    texto = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['creado']