from django.shortcuts import render

from .models import Contacts

# Create your views here.


def home(request):
    template_name = 'contacts/pages/home.html'
    contacts = Contacts.objects.order_by('-name',)
    context = {'contacts': contacts}
    return render(
        request,
        template_name,
        context
    )
