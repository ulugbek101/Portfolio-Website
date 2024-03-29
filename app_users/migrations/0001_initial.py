# Generated by Django 4.2.7 on 2023-11-26 14:43

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
                ('country_flag', models.ImageField(blank=True, null=True, upload_to='')),
                ('rate', models.IntegerField(choices=[(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)], max_length=1)),
                ('body', models.TextField()),
                ('verified', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
