from django.shortcuts import get_object_or_404, render

from .models import Contacts

# Create your views here.


def home(request):
    template_name = 'contacts/pages/home.html'
    contacts = Contacts.objects.order_by('name',)
    context = {'contacts': contacts}
    return render(
        request,
        template_name,
        context
    )


def contactDetail(request, id):
    template_name = 'contacts/pages/contact-detail.html'
    contact = get_object_or_404(Contacts, pk=id)
    context = {'contact': contact}

    return render(request, template_name, context)
