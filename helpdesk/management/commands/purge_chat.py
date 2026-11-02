from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from helpdesk.models import ChatMessage


class Command(BaseCommand):
    help = "Elimina las conversaciones del chat con mas de N dias (por defecto 90)."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=90)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        limite = timezone.now() - timedelta(days=options["days"])
        qs = ChatMessage.objects.filter(created__lt=limite)
        total = qs.count()
        if options["dry_run"]:
            self.stdout.write(f"[dry-run] Se borrarian {total} mensajes anteriores a {limite:%Y-%m-%d}.")
            return
        qs.delete()
        self.stdout.write(f"Borrados {total} mensajes anteriores a {limite:%Y-%m-%d}.")
