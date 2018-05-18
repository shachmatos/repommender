from django.db import models


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
    image = models.URLField(null=True)
    description = models.TextField(null=True)
    url = models.URLField(max_length=255)
    topics = models.TextField()
    languages = models.TextField()
    watchers_count = models.PositiveIntegerField()
    forks_count = models.PositiveIntegerField()
    open_issues = models.PositiveIntegerField()
    subscribers_count = models.PositiveIntegerField()
    updated_at = models.DateTimeField()
    pushed_at = models.DateTimeField()

    recommended = models.ManyToManyField('Repository', through='Recommendation', through_fields=('source','target'))


class Recommendation(models.Model):
    class Meta:
        db_table = "recommendations"
        unique_together = (('source', 'target'),)

    source = models.ForeignKey('Repository', models.CASCADE, 'source', db_index=True)
    target = models.ForeignKey('Repository', models.CASCADE, 'target', db_index=True)
    score = models.FloatField(max_length=64)


class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    preferred_languages = models.TextField(null=True)
    preferred_topics = models.TextField(null=True)


class UserRepositories(models.Model):
    user_id = models.ForeignKey('User', models.CASCADE, db_index=True)
    repo_id = models.ForeignKey('Repository', models.CASCADE, db_index=True)
