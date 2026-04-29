from django.contrib import admin
from django import forms
from .models import Comment

class CommentAdminForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 15,  # Altura en líneas
            'cols': 100,  # Ancho en caracteres
            'style': 'width: 100%;'  # O usar CSS
        })
    )
    
    class Meta:
        model = Comment
        fields = '__all__'

class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm
    list_display = ('user', 'post', 'created_at', 'approved_comment')
    list_filter = ('approved_comment', 'created_at')
    search_fields = ('user__username', 'comment', 'post__title')

admin.site.register(Comment, CommentAdmin)