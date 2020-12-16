from django.shortcuts import render, redirect
from .forms import SearchForm
from marvel.marvel import Marvel
from django.conf import settings
from .models import Comic
from django.core.files import File
from urllib.request import urlretrieve
from rest_framework.views import APIView


m = Marvel(settings.MARVEL_PUBLIC_KEY, settings.MARVEL_PRIVATE_KEY)


class SearchComics(APIView):
    def get(self, request):
        form = SearchForm()
        required_comics = []
        if 'title' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                cd = form.cleaned_data
                comics = m.comics.all()['data']['results']
                for comic in comics:
                    if cd['title'] in comic['title']:
                        required_comics.append(comic)
        return render(
            request,
            'search.html',
            {
                'form': form,
                'comics': required_comics,
            }
        )


class ViewComics(APIView):
    def get(self, request, id):
        comic = m.comics.get(id)['data']['results'][0]
        return render(
            request,
            'detailcomics.html',
            {
                'comic': comic,
                'id': id,
            }
        )

    def post(self, request, id):
        comic = m.comics.get(id)['data']['results'][0]

        try:
            Comic.objects.get(title=comic['title'])
        except Comic.DoesNotExist:
            extension = comic['thumbnail']['extension']
            filename = comic['thumbnail']['path'].split('/')[-1]
            path = comic['thumbnail']['path']

            f = open(urlretrieve(f'{path}.{extension}')[0], 'rb')

            filenames = []
            fi = []
            for i in comic['images']:
                extension = i['extension']
                filenames.append(i['path'].split('/')[-1])
                path = i['path']

                fi.append(open(urlretrieve(f'{path}.{extension}')[0], 'rb'))

            com = Comic.objects.create(
                title=comic['title'],
                description=comic['description'],
                datetime_created=comic['dates'][0]['date'],
                images=[] * len(fi),
                characters=[i['name'] for i in comic['characters']['items']],
                stories=[i['name'] for i in comic['stories']['items']],
            )

            com.thumbnail.save(
                filename,
                File(f),
            )

            for n, i in enumerate(com.images):
                i.save(
                    filenames[n],
                    File(fi[n])
                )

            com.save()

            f.close()
            for i in fi:
                i.close()

        return redirect(
            'detailcomics',
            id
        )


class ListMasterComics(APIView):
    def get(self, request):
        comics = Comic.objects.all()
        return render(
            request,
            'listcomics.html',
            {
                'comics': comics,
            }
        )


class MasterComic(APIView):
    def get(self, request, id):
        comic = Comic.objects.get(id=id)
        return render(
            request,
            'masterdetailcomics.html',
            {
                'comic': comic,
            }
        )

    def post(self, request, id):
        comic = Comic.objects.get(id=id)
        comic.delete()
        return redirect(
            'master',
        )