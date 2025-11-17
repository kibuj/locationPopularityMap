from django.db import models
from django.conf import settings

class Location(models.Model):
    name = models.CharField(max_length=255,unique=True, help_text="The name of the location")
    address = models.CharField(blank=True, null=True, max_length=255,help_text="The address of the location")
    coordinates = models.CharField(blank=True, null=True, max_length=255,help_text="The coordinates of the location")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # або models.CASCADE
        null=True,  # Дозволяє автору бути NULL (якщо юзера видалять)
        related_name='locations'  # Дозволяє отримати user.locations.all()
    )

    def __str__(self):
        return self.name
