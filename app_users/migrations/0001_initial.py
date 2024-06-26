# Generated by Django 4.2.11 on 2024-04-09 08:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('address', models.CharField(max_length=255)),
                ('profile_photo', models.ImageField(default='thedevu101-media/profile-photos/user-default.png', null=True, upload_to='thedevu101-media/profile-photo/user-default.png')),
                ('country_flag', models.ImageField(blank=True, null=True, upload_to='thedevu101-media/country-photos')),
                ('rate', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=5)),
                ('body', models.TextField()),
                ('verified', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created', 'verified'],
            },
        ),
    ]
