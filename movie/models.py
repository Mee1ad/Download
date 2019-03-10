from django.contrib.auth.models import AbstractUser
from django_mysql.models import ListCharField
from django_mysql.models import Model
from django.db import models
import json
from django.contrib.auth.validators import UnicodeUsernameValidator
# Create your models here.


class Movie(Model):
    def __str__(self):
        return self.imdb_id
    imdb_id = models.CharField(max_length=15)
    description = models.TextField()


class Link(Model):
    def __str__(self):
        return self.link
    imdb_id = models.CharField(max_length=15)
    link = models.TextField()
    quality = models.CharField(max_length=31)
    encoder = models.CharField(max_length=31)
    size = models.CharField(max_length=15)
