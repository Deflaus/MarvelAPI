from django.urls import path
from . import views
from .models import Comic


urlpatterns = [
    path('marvel/', views.SearchComics.as_view(), name='marvel'),
    path('marvel/<int:id>', views.ViewComics.as_view(), name='marvel-comic'),
    path('master/', views.ListMasterComics.as_view(), name='master'),
    path('master/<int:id>', views.MasterComic.as_view(), name='master-comic'),
]
