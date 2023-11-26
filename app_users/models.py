import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    RATE_CHOICES = (
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=255)
    profile_photo = models.ImageField(null=True, default='thedevu101-media/profile-photos/user-default.png', upload_to='thedevu101-media/profile-photo/user-default.png')
    country_flag = models.ImageField(null=True, blank=True, upload_to='thedevu101-media/country-photos')
    rate = models.IntegerField(choices=RATE_CHOICES, max_length=1)
    body = models.TextField()
    verified = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.body[:30]}"

