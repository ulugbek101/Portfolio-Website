# Generated by Django 5.1.2 on 2024-10-23 16:10

import django_ckeditor_5.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('title', models.CharField(max_length=255, unique=True)),
                ('link', models.URLField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(upload_to='thedevu101-media/projects')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, null=True)),
                ('body', django_ckeditor_5.fields.CKEditor5Field()),
                ('requests', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('tags', models.ManyToManyField(to='app_main.tag')),
            ],
            options={
                'ordering': ('created', 'requests'),
            },
        ),
    ]
