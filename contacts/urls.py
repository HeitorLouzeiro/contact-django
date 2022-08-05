from django.urls import path

from contacts.views import home

urlpatterns = [
    path('', home),
]
