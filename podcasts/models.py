from unittest.main import MODULE_EXAMPLES
from django.db import models
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title

class Episode(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE,null=True)
    description = models.TextField()
    published_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    podcast_name = models.CharField(max_length=100)
    guid = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Episode"
        verbose_name_plural = "Episodes"
        ordering = ['-published_date']

    def __str__(self):
        return f"{self.podcast_name}: {self.title}"





class User(AbstractUser):
    genres = models.ManyToManyField(Category, blank=True)
    favorites = models.ManyToManyField(
        Episode, blank=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    like = models.ForeignKey(Episode, related_name='likes', on_delete=models.CASCADE)

    
