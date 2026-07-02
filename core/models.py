from django.db import models

class Resena(models.Model):
    autor = models.CharField(max_length=100)
    texto = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    foto_url = models.URLField(blank=True, null=True)
    fecha_relativa = models.CharField(max_length=50, blank=True)  # ej: "Hace 5 meses"
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['orden', '-id']
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"

    def __str__(self):
        return f"{self.autor} ({self.rating}★)"
    

class ResenasConfig(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.8)
    total = models.PositiveSmallIntegerField(default=5)
    ultima_sync = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuración de Reseñas"
        verbose_name_plural = "Configuración de Reseñas"

    def __str__(self):
        return f"Rating global: {self.rating}/5 ({self.total} reseñas) — última sync: {self.ultima_sync:%d/%m/%Y}"

    def save(self, *args, **kwargs):
        self.pk = 1  # fuerza a que solo exista una fila (singleton)
        super().save(*args, **kwargs)

    @classmethod
    def get_config(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj