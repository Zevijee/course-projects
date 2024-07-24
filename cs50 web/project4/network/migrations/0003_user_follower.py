# Generated by Django 4.2.2 on 2023-06-13 15:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0002_post"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="follower",
            field=models.ManyToManyField(
                blank=True, related_name="following", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
