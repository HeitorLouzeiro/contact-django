from django.urls import path

from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.home, name='home'),
    path(
        'search/',
        views.search,
        name="search"
    ),
    path(
        'contact-detail/<int:id>/',
        views.contactDetail,
        name='contact-detail'
    ),
]
