from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    about = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username