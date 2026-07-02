import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Resena, ResenasConfig


class Command(BaseCommand):
    help = "Sincroniza reseñas de Google Places con la base de datos local (ejecutar semanalmente vía cron)"

    def handle(self, *args, **options):
        url = f"https://places.googleapis.com/v1/places/{settings.GOOGLE_PLACE_ID}"
        headers = {
            "X-Goog-Api-Key": settings.GOOGLE_PLACES_API_KEY,
            "X-Goog-FieldMask": "rating,userRatingCount,reviews",
        }
        params = {"languageCode": "es"}

        try:
            r = requests.get(url, headers=headers, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error llamando a Places API: {e}"))
            return

        # --- Actualizar rating/total globales ---
        config = ResenasConfig.get_config()
        config.rating = data.get("rating", config.rating)
        config.total = data.get("userRatingCount", config.total)
        config.save()

        # --- Actualizar reseñas individuales ---
        google_reviews = [
            rev for rev in data.get("reviews", [])
            if rev.get("text", {}).get("text")
        ]

        creadas, actualizadas = 0, 0

        for i, rev in enumerate(google_reviews):
            autor = rev.get("authorAttribution", {}).get("displayName", "")
            texto = rev.get("text", {}).get("text", "")
            rating = rev.get("rating", 5)
            foto_url = rev.get("authorAttribution", {}).get("photoUri", "")
            fecha_relativa = rev.get("relativePublishTimeDescription", "")

            obj, created = Resena.objects.update_or_create(
                autor=autor,
                texto=texto,
                defaults={
                    "rating": rating,
                    "foto_url": foto_url,
                    "fecha_relativa": fecha_relativa,
                    "orden": i,
                }
            )
            creadas += 1 if created else 0
            actualizadas += 0 if created else 1

        self.stdout.write(self.style.SUCCESS(
            f"Sync completada: {creadas} reseñas nuevas, {actualizadas} actualizadas. "
            f"Rating: {config.rating}/5 ({config.total} totales)."
        ))