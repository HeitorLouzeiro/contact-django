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

    def test_contact_template_load_contact_favorite_false(self):
        # Test is contact favorite False
        self.make_contact(favorite=False)
        response = self.client.get(reverse('contacts:home'))
        content = response.content.decode('utf-8')

        # Check if contatcts favorite false
        self.assertIn(
            '<i class="bi bi-star"></i>', content)

    def test_contact_template_load_contact_favorite_true(self):
        # Test is contact favorite True
        self.make_contact(favorite=True)
        response = self.client.get(reverse('contacts:home'))
        content = response.content.decode('utf-8')

        # Check if contatcts favorite True
        self.assertIn(
            '<i class="bi bi-star-fill"></i>', content)

    def test_contact_home_load_contacts(self):
        # Need a contacts for this test
        self.make_contact()
        response = self.client.get(reverse('contacts:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['contacts']

        # Check if one contatcts exists
        self.assertIn('user', content)

        self.assertEqual(len(response_context_recipes), 1)

    def test_contact_contactDetail_view_function_is_correct(self):
        view = resolve(reverse('contacts:contact-detail', kwargs={'id': 1}))
        self.assertIs(view.func, views.contactDetail)

    def test_contact_contactDetail_view_returns_404_is_no_contact_found(self):
        response = self.client.get(
            reverse('contacts:contact-detail', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_contact_contactDetail_load_contacts(self):
        new_name = 'Joao'
        # Need a contacts for this test
        self.make_contact(name=new_name)
        response = self.client.get(
            reverse(
                'contacts:contact-detail',
                kwargs={
                    'id': 1
                }
            )
        )
        content = response.content.decode('utf-8')

        # Check if one contatcts exists
        self.assertIn(new_name, content)

    def test_contact_search_view_function_is_correct(self):
        view = resolve(reverse('contacts:search'))
        self.assertIs(view.func, views.search)

    def test_contact_search_loads_correct_template(self):
        response = self.client.get(reverse('contacts:search') + '?q=test')
        self.assertTemplateUsed(response, 'contacts/pages/home.html')

    def test_contact_search_raises_404_if_no_search_term(self):
        url = reverse('contacts:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
