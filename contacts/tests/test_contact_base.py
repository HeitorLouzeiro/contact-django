from contacts.models import Contacts
from django.test import TestCase


class ContactTestBase(TestCase):
    def setUp(self) -> None:
        contacts = self.make_contact
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def make_contact(
        self,
        name='user',
        last_name='Last name',
        email='email@enmail.com',
        telephone='89965452',
        note='Is note',
        favorite=False,

    ):
        return Contacts.objects.create(
            name=name,
            last_name=last_name,
            email=email,
            telephone=telephone,
            note=note,
            favorite=favorite,
        )
