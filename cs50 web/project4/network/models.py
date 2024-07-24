from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name="following", blank=True)

    def serialize(self):
        return {
            "user_id": self.id,
            "username": self.username,
            "followers": self.followers.count(),
            "following": self.following.count()
        }


class Post(models.Model):
    poster = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(max_length=2000)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "posterId": self.poster.id,
            "text": self.text,
            "likes": self.likes,
            "liked_by": [user.id for user in self.liked_by.all()],
            "timestamp": self.timestamp
        }