from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    display_name = models.CharField(max_length=50)
    short_description = models.CharField(max_length=255)


class Recommendation(models.Model):
    class Meta:
        unique_together = (('source', 'target'),)

    source = models.IntegerField(db_index=True)
    target = models.IntegerField(db_index=True)
    score = models.FloatField(max_length=64)


