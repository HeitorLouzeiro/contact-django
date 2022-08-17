import pandas as pd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactForm
from .models import Contacts, ExcelFile


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
    contact.delete()
    messages.success(request, 'Contact Deleted successfully.')
    return redirect(reverse('contacts:home'))


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


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def importContacts(request):
    if request.method == 'POST':
        file = request.FILES['files']
        # checking file extension
        if not file.name.endswith('.xlsx'):
            messages.error(request, 'This is not xlsx file')
            return render(request, 'contacts/pages/contact-import.html')
        # putting file in database
        obj = ExcelFile.objects.create(
            file=file
        )
        # getting the file location
        path = str(obj.file)
        # opening excel with pandas
        df = pd.read_excel(path)
        # handling empty columns
        df = df.fillna('')
        # empty list
        data = []
        try:
            for row in df.values:
                # putting execel values ​​with the Contacts model fields
                contact = Contacts(
                    name=row[1],
                    last_name=row[2],
                    email=row[3],
                    telephone=row[4],
                    favorite=row[5],
                    note=row[6],
                    create=row[7],
                    user=request.user,
                )
                # adding fields in a data list.
                data.append(contact)
            # creating data and saving to database.
            Contacts.objects.bulk_create(data)
            # deleting file from database and excel folder.
            obj.delete()
            # sending to the home folder with the imported data.
            messages.success(request, 'Contacts imported successfully.')
            return redirect(reverse('contacts:home'))
        except Exception:
            obj.delete()
            messages.error(
                request, 'Erro ao importar o arquivo excel,'
                'verifique se o excel está com os dados corretos.'
            )
            return render(request, 'contacts/pages/contact-import.html')

    return render(request, 'contacts/pages/contact-import.html')


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def contactsExport(request):
    # selected data according to user
    objs = Contacts.objects.filter(user=request.user)
    data = []
    # checking if there is a record in the database
    if len(objs) > 0:
        for obj in objs:
            # accenting with in excel
            data.append({
                "name": obj.name,
                "last_name": obj.last_name,
                "email": obj.email,
                "telephone": obj.telephone,
                "favorite": obj.favorite,
                "note": obj.note,
                "create": obj.create,
            })
        # doing data processing with pandas
        df = pd.DataFrame(data)
        # downloading to the person's computer.
        response = HttpResponse(content_type='text/xlsx')
        response['Content-Disposition'] = 'attachment; \
        filename="contacts.xlsx"'

        df.to_excel(response)
        return response
    else:
        messages.info(
            request, 'Create a contact to do the export.'
        )
        return render(request, 'contacts/pages/home.html')
