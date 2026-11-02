from django.db import models


class ChatMessage(models.Model):
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    session_key = models.CharField(max_length=40, blank=True, db_index=True)
    ip_hash = models.CharField(max_length=16, blank=True)
    language = models.CharField(max_length=5, blank=True)
    user_message = models.TextField()
    assistant_reply = models.TextField(blank=True)
    flagged = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.created:%Y-%m-%d %H:%M} {self.user_message[:50]}"