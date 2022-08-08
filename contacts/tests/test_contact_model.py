from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_contact_base import ContactTestBase


class ContactModelTest(ContactTestBase):
    def setUp(self) -> None:
        self.contact = self.make_contact()
        return super().setUp()

    # Example 1
    def test_contact_name_raise_error_if_name_has_more_than_20_chars(self):
        self.contact.name = 'A' * 21

        with self.assertRaises(ValidationError):
            self.contact.full_clean()

    # Example 2
    @parameterized.expand([
        ('name', 20),
        ('last_name', 30),
        ('email', 50), ])
    def test_contact_filds_max_legth(self, field, max_length):
        setattr(self.contact, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.contact.full_clean()
