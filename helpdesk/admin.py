from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('created', 'language', 'flagged', 'short_message')
    list_filter = ('flagged', 'language', 'created')
    search_fields = ('user_message', 'assistant_reply')
    date_hierarchy = 'created'

    def short_message(self, obj):
        return obj.user_message[:80]
    short_message.short_description = 'Mensaje'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False