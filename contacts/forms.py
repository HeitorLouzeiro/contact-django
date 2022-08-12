
from django import forms

from contacts.models import Contacts


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contacts
        fields = [
            'name',
            'last_name',
            'email',
            'telephone',
            'favorite',
            'note',
        ]
