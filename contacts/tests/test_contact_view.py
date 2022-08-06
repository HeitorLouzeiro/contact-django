from contacts import views
from django.test import TestCase
from django.urls import resolve, reverse


class ContactViewsTest(TestCase):
    def test_contact_home_view_function_is_correct(self):
        view = resolve(reverse('contacts:home'))
        self.assertIs(view.func, views.home)

    def test_contact_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('contacts:home'))
        self.assertEqual(response.status_code, 200)

    def test_contact_home_view_load_correct_template(self):
        response = self.client.get(reverse('contacts:home'))
        self.assertTemplateUsed(response, 'contacts/pages/home.html')

    def test_contact_home_template_shows_no_contact_found_if_no_contacts(self):
        response = self.client.get(reverse('contacts:home'))
        self.assertIn(
            'Contacts',
            response.content.decode('utf-8')
        )

    def test_contact_contactDetail_view_function_is_correct(self):
        view = resolve(reverse('contacts:contact-detail', kwargs={'id': 1}))
        self.assertIs(view.func, views.contactDetail)

    def test_contact_contactDetail_view_returns_404_is_no_contact_found(self):
        response = self.client.get(
            reverse('contacts:contact-detail', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_contact_home_template_shows_no_contact_found_if_no_contacts_table(self):
        response = self.client.get(reverse('contacts:home'))
        self.assertIn(
            'No Contacts found here',
            response.content.decode('utf-8')
        )
