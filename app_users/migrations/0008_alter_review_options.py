# Generated by Django 4.2.7 on 2023-12-16 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0007_alter_review_rate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created', 'verified']},
        ),
    ]
