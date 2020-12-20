from django.shortcuts import render, redirect
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .forms import SearchForm
from .comics_services import get_comics_from_marvel_API_with_given_title, \
    save_comic_in_bd, \
    get_comic_from_marvel_API_with_given_id, \
    get_all_comics_from_bd, \
    get_comic_from_bd_with_given_id, \
    delete_comic_from_bd, \
    get_thumbnail_from_bd_with_given_comic, \
    get_linked_images_from_bd_with_given_comic, \
    get_characters_from_bd_with_given_comic, \
    get_stories_from_bd_with_given_comic


class SearchComics(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        required_comics = []

        form = SearchForm()
        page = request.GET.get('page')
        search_title = ''

        if 'title' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                cd = form.cleaned_data
                required_comics = get_comics_from_marvel_API_with_given_title(cd['title'])
                search_title = cd['title']

        paginator = Paginator(required_comics, 3)

        try:
            comics = paginator.page(page)
        except PageNotAnInteger:
            comics = paginator.page(1)
        except EmptyPage:
            comics = paginator.page(paginator.num_pages)

        return render(
            request,
            'comics/search.html',
            {
                'search_title': search_title,
                'page': page,
                'form': form,
                'comics': comics,
            }
        )


class MarvelComic(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        comic = get_comic_from_marvel_API_with_given_id(id)

        return render(
            request,
            'comics/detailcomics.html',
            {
                'comic': comic,
                'id': id,
            }
        )

    def post(self, request, id):
        save_comic_in_bd(request.user, id)

        return redirect(
            'marvel-comic',
            id
        )


class ListMasterComics(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        comics = get_all_comics_from_bd(request.user)

        return render(
            request,
            'comics/listcomics.html',
            {
                'comics': comics,
            }
        )


class MasterComic(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        comic = get_comic_from_bd_with_given_id(request.user, id)[0]
        thumbnail = get_thumbnail_from_bd_with_given_comic(comic)
        linkedimages = get_linked_images_from_bd_with_given_comic(comic)
        characters = get_characters_from_bd_with_given_comic(comic)
        stories = get_stories_from_bd_with_given_comic(comic)

        return render(
            request,
            'comics/masterdetailcomics.html',
            {
                'comic': comic,
                'thumbnail': thumbnail,
                'linkedimages': linkedimages,
                'characters': characters,
                'stories': stories,
            }
        )

    def post(self, request, id):
        delete_comic_from_bd(request.user, id)

        return redirect(
            'master',
        )