from django.shortcuts import render, redirect
from rest_framework.views import APIView

from .forms import SearchForm
from .comics_services import get_comics_from_marvel_API_with_given_title, \
    save_comic_in_bd, get_comic_from_marvel_API_with_given_id, \
    get_all_comics_from_bd, get_comic_from_bd_with_given_id, \
    delete_comic_from_bd


class SearchComics(APIView):
    def get(self, request):
        required_comics = []

        form = SearchForm()

        if 'title' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                cd = form.cleaned_data
                required_comics = get_comics_from_marvel_API_with_given_title(cd['title'])

        return render(
            request,
            'search.html',
            {
                'form': form,
                'comics': required_comics,
            }
        )


class MarvelComic(APIView):
    def get(self, request, id):
        comic = get_comic_from_marvel_API_with_given_id(id)

        return render(
            request,
            'detailcomics.html',
            {
                'comic': comic,
                'id': id,
            }
        )

    def post(self, request, id):
        save_comic_in_bd(id)

        return redirect(
            'marvel-comic',
            id
        )


class ListMasterComics(APIView):
    def get(self, request):
        comics = get_all_comics_from_bd
        return render(
            request,
            'listcomics.html',
            {
                'comics': comics,
            }
        )


class MasterComic(APIView):
    def get(self, request, id):
        comic = get_comic_from_bd_with_given_id(id)

        return render(
            request,
            'masterdetailcomics.html',
            {
                'comic': comic,
            }
        )

    def post(self, request, id):
        delete_comic_from_bd(id)

        return redirect(
            'master',
        )