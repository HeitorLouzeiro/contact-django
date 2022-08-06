from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class ContactUrlsTest(TestCase):
    def test_if_the_home_url_is_correct(self):
        url = reverse('contacts:home')
        self.assertEqual(url, '/')

    def test_if_the_detail_url_is_correct(self):
        url = reverse('contacts:contact-detail', kwargs={'id': 1})
        self.assertEqual(url, '/contact-detail/1/')
