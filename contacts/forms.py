
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
        widgets = {
            'telephone': forms.TextInput(
                attrs={
                    'data-mask': '(00) 0.0000-0000'}
            )
        }
