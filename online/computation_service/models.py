from django.db import models
from github import Github


class Topic(models.Model):
    class Meta:
        db_table = "topics"
    name = models.CharField(max_length=50, primary_key=True)
    display_name = models.CharField(max_length=50)
    short_description = models.CharField(max_length=255)


class Language(models.Model):
    class Meta:
        db_table = "languages"

    name = models.CharField(max_length=50, primary_key=True)


class Repository(models.Model):
    class Meta:
        db_table = "repositories"

    id = models.PositiveIntegerField(primary_key=True)
    size = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    topics = models.TextField()
    languages = models.TextField()
    watchers_count = models.PositiveIntegerField()
    forks_count = models.PositiveIntegerField()
    open_issues = models.PositiveIntegerField()
    subscribers_count = models.PositiveIntegerField()
    updated_at = models.DateTimeField()
    pushed_at = models.DateTimeField()


class Recommendation(models.Model):
    class Meta:
        db_table = "recommendations"
        unique_together = (('source', 'target'),)

    source = models.IntegerField(db_index=True)
    target = models.IntegerField(db_index=True)
    score = models.FloatField(max_length=64)

    def get_target_repo(self):
        g = Github()
        return g.get_repo(self.target)

    def __str__(self):
        return str(self.source) + " -> " + str(self.target) + " | Score: " + str(self.score)
