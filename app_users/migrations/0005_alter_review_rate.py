# Generated by Django 4.2.7 on 2023-11-26 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0004_alter_review_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rate',
            field=models.IntegerField(choices=[(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]),
        ),
    ]
