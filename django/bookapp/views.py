from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def home(request):
    if request.user.is_authenticated:
        return redirect('/booklist')
    return redirect('/login')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/booklist')
    else:
        form = AuthenticationForm()
    return render(request, 'bookapp/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/booking')
    else:
        form = UserCreationForm()
    return render(request, 'bookapp/register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/login')
    # logout(redirect('/login'))


