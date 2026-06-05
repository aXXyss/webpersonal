from django.contrib.auth.models import User
from django.db import models
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='users/pictures', blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    activation_token = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.user.username