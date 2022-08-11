from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import render

from .models import Contacts


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def home(request):
    template_name = 'contacts/pages/home.html'
    contacts = Contacts.objects.filter(user=request.user).order_by('name',)
    contactsCount = contacts.count()

    context = {
        'contacts': contacts,
        'contactsCount': contactsCount,
    }
    return render(
        request,
        template_name,
        context
    )


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def contactDetail(request, id):
    template_name = 'contacts/pages/contact-detail.html'
    contact = Contacts.objects.filter(
        user=request.user,
        pk=id,
    ).first()

    if not contact:
        raise Http404()
    context = {'contact': contact}

    return render(request, template_name, context)


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def search(request):
    search_term = request.GET.get('q', '').strip()
    template_name = 'contacts/pages/home.html'

    if not search_term:
        raise Http404()

    contacts = Contacts.objects.filter(
        Q(
            Q(name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(email__icontains=search_term) |
            Q(telephone__icontains=search_term)
        )
    ).order_by('name',)
    contactsCount = contacts.count()

    context = {
        'contacts': contacts,
        'search_term': search_term,
        'additional_url_query': f'&q={search_term}',
        'contactsCount': contactsCount,
    }

    return render(request, template_name, context)
