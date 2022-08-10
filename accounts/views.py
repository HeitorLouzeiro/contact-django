from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, RegisterForm

# Create your views here.


def loginUser(request):
    if request.method == 'GET':
        tamplate_name = 'accounts/pages/login.html'
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, tamplate_name, context)

    if request.method == 'POST':
        form = LoginForm(request.POST or None)

        if form.is_valid():
            authenticated_user = authenticate(
                username=form.cleaned_data.get('username', ''),
                password=form.cleaned_data.get('password', ''),
            )
            if authenticated_user is not None:
                login(request, authenticated_user)
            else:
                messages.error(request, 'Invalid username or password')

    return redirect(reverse('contacts:home'))


def LogoutUser(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')

    return redirect(reverse('accounts:loginUser'))


def register(request):
    if request.method == 'GET':
        template_name = 'accounts/pages/register.html'
        form = RegisterForm()
        context = {
            'form': form,
        }
        return render(request, template_name, context)

    if request.method == 'POST':
        template_name = 'accounts/pages/register.html'
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered SuccessFully")
            return redirect('accounts:login')

        context = {
            'form': form,
        }

        return render(request, template_name, context)
