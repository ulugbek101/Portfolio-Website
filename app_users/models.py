import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    RATE_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=255)
    profile_photo = models.ImageField(null=True, default='thedevu101-media/profile-photos/user-default.png', upload_to='profile-photos/')
    country_flag = models.ImageField(null=True, blank=True, upload_to='country-photos/')
    rate = models.IntegerField(choices=RATE_CHOICES, default=5)
    body = models.TextField()
    verified = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def to_representation(self):
        return self.__str__()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.body[:30]}"
    
    class Meta:
        ordering = ['-created', 'verified']

