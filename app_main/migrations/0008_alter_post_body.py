# Generated by Django 4.2.7 on 2023-12-20 04:41

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0007_rename_tag_post_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=markdownx.models.MarkdownxField(),
        ),
    ]
