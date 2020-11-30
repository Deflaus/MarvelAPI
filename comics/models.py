from django.db import models
from django.contrib.postgres.fields import ArrayField


class Comics(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    datetime_created = models.DateTimeField()
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    images = ArrayField(models.ImageField(upload_to='images/'), blank=True, null=True)
    characters = ArrayField(models.CharField(max_length=200))
    stories = ArrayField(models.CharField(max_length=200))

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return f'Комикс {self.title}'
