from django.db import models
from django.contrib.auth.models import User


class Comic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=User.objects.get(username='daniil').pk)
    title = models.CharField(max_length=200)
    description = models.TextField()
    datetime_created = models.DateTimeField()

    class Meta:
        db_table = 'comics'
        ordering = ('title',)

    def __str__(self):
        return f'Комикс {self.title}'


class LinkedImage(models.Model):
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True)

    class Meta:
        db_table = 'linkedimages'

    def __str__(self):
        return f'Связанное изображение с комиксом {self.comic}'


class Thumbnail(models.Model):
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)

    class Meta:
        db_table = 'thumbnails'

    def __str__(self):
        return f'Обложка к комиксу {self.comic}'


class Character(models.Model):
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'characters'

    def __str__(self):
        return f'Персонаж {self.name} в комиксе {self.comic}'


class Storie(models.Model):
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    class Meta:
        db_table = 'stories'

    def __str__(self):
        return f'Storie {self.title} в комиксе {self.comic}'
