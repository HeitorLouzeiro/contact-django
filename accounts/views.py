
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, RegisterForm

# Create your views here.


def loginUser(request):
    if request.method == 'GET':
        tamplate_name = 'accounts/pages/login.html'
        form = LoginForm()
        return render(request, tamplate_name, {'form': form})

    if request.method == 'POST':
        form = LoginForm(request.POST or None)

        authenticated_user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )

        if authenticated_user is not None:
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect(reverse('contacts:home'))


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def LogoutUser(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('accounts:loginUser'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('accounts:loginUser'))

    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect(reverse('accounts:loginUser'))


def register(request):
    tamplate_name = 'accounts/pages/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "Registered Successfully !")
            return redirect('accounts:loginUser')
        else:
            return render(request, tamplate_name, {'form': form})
    else:
        form = RegisterForm()
        return render(request, tamplate_name, {'form': form})
