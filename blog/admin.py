from django.contrib import admin
from .models import Post, UserProfile

admin.site.register(UserProfile)
admin.site.register(Post)


class BlogAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('author', 'title', 'published_date')
    list_filter = ('created', 'modified')
        
        
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('url', )
        form = super(PostAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        form.base_fields['profile'].initial = request.user.profile
        return form


