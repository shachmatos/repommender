from django.db import models
from django.utils.datetime_safe import datetime


class Developer (models.Model):
    id: models.IntegerField(primary_key=True)
    name: models.CharField(unique=True, max_length=50)
    created_at: models.DateTimeField(default=datetime.now())


class Repository (models.Model):
    id: models.IntegerField(primary_key=True)
    owner_id: models.ForeignKey('Developer', on_delete=models.CASCADE)
    name: models.CharField(max_length=100)


