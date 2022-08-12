from django.urls import path

from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.home, name='home'),
    path(
        'search/',
        views.search,
        name='search'
    ),
    path(
        'contact-register/',
        views.contactRegister,
        name='contact-register'
    ),
    path(
        'contact-detail/<int:id>/',
        views.contactDetail,
        name='contact-detail'
    ),
    path(
        'contact-edit/<int:id>/',
        views.contactEdit,
        name='contact-edit'
    ),
    path(
        'contact-delete/<int:id>/',
        views.contactDelete,
        name='contact-delete'
    ),
]
