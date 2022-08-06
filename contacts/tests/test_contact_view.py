from contacts import views
from django.test import TestCase
from django.urls import resolve, reverse


class ContactViewsTest(TestCase):
    def test_contact_home_view_function_is_correct(self):
        view = resolve(reverse('contacts:home'))
        self.assertIs(view.func, views.home)

    def test_contact_contactDetail_view_function_is_correct(self):
        view = resolve(reverse('contacts:contact-detail', kwargs={'id': 1}))
        self.assertIs(view.func, views.contactDetail)
