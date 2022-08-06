from pydoc import resolve

from django.test import TestCase
from django.urls import resolve, reverse

from contacts import views


# Create your tests here.
class ContactUrlsTest(TestCase):
    def test_if_the_home_url_is_correct(self):
        url = reverse('contacts:home')
        self.assertEqual(url, '/')

    def test_if_the_contactDetail_url_is_correct(self):
        url = reverse('contacts:contact-detail', kwargs={'id': 1})
        self.assertEqual(url, '/contact-detail/1/')


class ContactViewsTest(TestCase):
    def test_contact_home_view_function_is_correct(self):
        view = resolve(reverse('contacts:home'))
        self.assertIs(view.func, views.home)

    def test_contact_contactDetail_view_function_is_correct(self):
        view = resolve(reverse('contacts:contact-detail', kwargs={'id': 1}))
        self.assertIs(view.func, views.contactDetail)
