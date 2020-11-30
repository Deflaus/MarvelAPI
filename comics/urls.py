from django.urls import path
from .views import marvel, master, detailcomics, savecomics, masterdetailcomic, deletecomic
from .models import Comics


urlpatterns = [
    path('marvel/', marvel, name='marvel'),
    path('marvel/<int:id>', detailcomics, name='detailcomics'),
    path('marvel/<int:id>/save/', savecomics, name='savecomics'),
    path('master/', master, name='master'),
    path('master/<int:id>', masterdetailcomic, name='masterdetailcomic'),
    path('master/<int:id>/delete', deletecomic, name='deletecomic'),
]
