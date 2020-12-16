from django.conf import settings
from django.core.files import File

from .models import Comic, Thumbnail, LinkedImage, Character, Storie

from marvel.marvel import Marvel
from urllib.request import urlretrieve


m = Marvel(settings.MARVEL_PUBLIC_KEY, settings.MARVEL_PRIVATE_KEY)


'''Получить все комиксы с сайта Marvel'''
def _get_all_comics_from_marvel_API():
    return m.comics.all()['data']['results']


'''Получить комиксы с сайта Marvel по части его названия'''
def get_comics_from_marvel_API_with_given_title(title):
    comics = _get_all_comics_from_marvel_API()
    required_comics = []

    for comic in comics:
        if title in comic['title']:
            required_comics.append(comic)

    return required_comics


'''Получить комикс с сайта Marvel по его id'''
def get_comic_from_marvel_API_with_given_id(id):
    return m.comics.get(id)['data']['results'][0]


'''Получить комикс с базы данных по его названию'''
def get_comic_from_bd_with_given_title(title):
    return Comic.objects.filter(title=title)


'''Сохранить комикс в базу данных'''
def save_comic_in_bd(comic_from_marvel_API_id):
    comic_from_marvel_API = get_comic_from_marvel_API_with_given_id(comic_from_marvel_API_id)
    comic_from_bd = Comic.objects.create(
        title=comic_from_marvel_API['title'],
        description=comic_from_marvel_API['description'],
        datetime_created=comic_from_marvel_API['dates'][0]['date'],
    )

    _save_thumbnail_in_bd(
        comic_from_bd, comic_from_marvel_API['thumbnail']['path'],
        comic_from_marvel_API['thumbnail']['extension']
    )

    for i in comic_from_marvel_API['images']:
        _save_linked_image_in_bd(comic_from_bd, i['path'], i['extension'])

    for i in comic_from_marvel_API['characters']['items']:
        _save_character_in_bd(comic_from_bd, i['name'])

    for i in comic_from_marvel_API['stories']['items']:
        _save_storie_in_bd(comic_from_bd, i['name'])


'''Сохранить изображение по его url(path, extension) во временный файл'''
def _get_temporary_image(path, extension):
    return open(urlretrieve(f'{path}.{extension}')[0], 'rb')


'''Сохранить обложку комикса в базу данных'''
def _save_thumbnail_in_bd(comic, path, extension):
    f = _get_temporary_image(path, extension)
    thumbnail = Thumbnail.objects.create(comic=comic)
    thumbnail.thumbnail.save(f'{path.split("/")[-1]}.{extension}', File(f))


'''Сохранить изображение, связанное с комиксом в базу данных'''
def _save_linked_image_in_bd(comic, path, extension):
    f = _get_temporary_image(path, extension)
    image = LinkedImage.objects.create(comic=comic)
    image.image.save(f'{path.split("/")[-1]}.{extension}', File(f))


'''Сохранить персонажа комикса в базу данных'''
def _save_character_in_bd(comic, name):
    Character.objects.create(comic=comic, name=name)


'''Сохранить Storie комикса в его базу данных'''
def _save_storie_in_bd(comic, title):
    Storie.objects.create(comic=comic, title=title)


'''Получить все комиксы из базы данных'''
def get_all_comics_from_bd():
    return Comic.objects.all()


'''Получить комикс из базы данных по его id'''
def get_comic_from_bd_with_given_id(id):
    return Comic.objects.filter(id=id)


'''Удалить комикс из базы данных по его id'''
def delete_comic_from_bd(id):
    comic = get_comic_from_bd_with_given_id(id)
    comic.delete()


def get_thumbnail_from_bd(comic):
    return Thumbnail.objects.filter(comic=comic)
