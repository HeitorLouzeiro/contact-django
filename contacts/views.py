from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactForm
from .models import Contacts


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def home(request):
    template_name = 'contacts/pages/home.html'
    contacts = Contacts.objects.filter(
        user=request.user).order_by('-favorite', 'name',)
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
def contactRegister(request):
    template_name = 'contacts/pages/contact-register.html'
    form = ContactForm(request.POST or None)
    if form.is_valid():
        contact = form.save(commit=False)

        contact.user = request.user
        contact.save()

        return redirect(reverse('contacts:contact-detail', args=(contact.id,)))

    return render(request, template_name, {
        'form': form,
    })


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def contactEdit(request, id):
    template_name = 'contacts/pages/contact-edit.html'

    contact = Contacts.objects.filter(user=request.user, pk=id,).first()

    if not contact:
        raise Http404()

    form = ContactForm(request.POST or None, instance=contact)
    if form.is_valid():
        contact = form.save(commit=False)

        contact.user = request.user
        contact.save()
        messages.success(request, 'Your contact has been successfully edited!')
        return redirect(reverse('contacts:contact-detail', args=(contact.id,)))

    return render(request, template_name, {'form': form, })


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def contactDelete(request, id):
    if not request.POST:
        raise Http404()

    contact = Contacts.objects.filter(
        user=request.user,
        pk=id,
    ).first()

    if not contact:
        raise Http404()

    return redirect(reverse('contacts:contact-detail', args=(contact.id,)))


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
