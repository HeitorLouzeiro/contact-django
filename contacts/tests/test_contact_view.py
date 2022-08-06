from contacts import views
from django.urls import resolve, reverse

from .test_contact_base import ContactTestBase


class ContactViewsTest(ContactTestBase):

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

    def test_contact_home_template_shows_no_found_contacts_table(self):
        response = self.client.get(reverse('contacts:home'))
        self.assertIn(
            'No Contacts found here',
            response.content.decode('utf-8')
        )

    def test_contact_home_load_contacts(self):
        # Need a contacts for this test
        self.make_contact()
        response = self.client.get(reverse('contacts:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['contacts']

        # Check if one contatcts exists
        self.assertIn('user', content)
        self.assertIn('Last name', content)
        self.assertIn('email@enmail.com', content)
        self.assertIn('89965452', content)

        self.assertEqual(len(response_context_recipes), 1)

    def test_contact_contactDetail_view_function_is_correct(self):
        view = resolve(reverse('contacts:contact-detail', kwargs={'id': 1}))
        self.assertIs(view.func, views.contactDetail)

    def test_contact_contactDetail_view_returns_404_is_no_contact_found(self):
        response = self.client.get(
            reverse('contacts:contact-detail', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)
