from memoapp.models import MemoModel, MyUser
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout

from memoapp.forms import LoginForm

# Create your views here.

def signupview(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            MyUser.objects.create_user(username, password)
            return redirect('signin')
    return render(request, 'memoapp/signup.html', {'form': form})


def signinview(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('memoapp/list.html')
        else:
            return render(request, 'memoapp/signin.html', {})
    return render(request, 'memoapp/signin.html', {})
