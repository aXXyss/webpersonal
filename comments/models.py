from django.db import models
from django.contrib.auth.models import User
from blog.models import Post
from users.models import Profile  # Importación correcta

class Comment(models.Model):
    """Comment model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment