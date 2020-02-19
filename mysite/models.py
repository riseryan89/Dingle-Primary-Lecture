from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django_mysql.models import ListCharField


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comics(models.Model):
    title = models.CharField(default="", max_length=200, unique=True)
    author = models.CharField(default="", max_length=20)
    image_path = models.CharField(default="", max_length=255)
    catches = models.CharField(default="", max_length=255)
    title_code = models.CharField(default="", max_length=100)
    comic_code = models.CharField(default="", max_length=100)


class ComicsDetail(models.Model):
    comic = models.ForeignKey(Comics, on_delete=models.CASCADE, null=True)
    episode = models.IntegerField(default=1)
    pub_datetime = models.DateField(default=timezone.now)
    comic_imgs = ListCharField(
        base_field=models.CharField(max_length=20),
        size=12,
        max_length=251
    )
