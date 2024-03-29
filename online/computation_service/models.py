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


class Recommendation(models.Model):
    class Meta:
        db_table = "recommendations"
        unique_together = (('user', 'source', 'target'),)

    user = models.ForeignKey('User', models.CASCADE, db_index=True)
    source = models.PositiveIntegerField()
    target = models.ForeignKey('Repository', models.CASCADE, 'target', db_index=True)
    channel_type = models.CharField(max_length=255)
    score = models.FloatField(max_length=64)


class User(models.Model):
    class Meta:
        db_table = "users"

    id = models.PositiveIntegerField(primary_key=True)
    login = models.CharField(unique=True, max_length=50)
    avatar_url = models.URLField()
    preferred_topics = models.TextField(null=True)


class UserRepository(models.Model):
    class Meta:
        db_table = "user_repositories"
    user = models.ForeignKey('User', models.CASCADE, db_index=True)
    repo = models.ForeignKey('Repository', models.CASCADE, db_index=True)
    contributions = models.PositiveIntegerField(default=0)
