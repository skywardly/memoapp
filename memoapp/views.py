from memoapp.models import MemoModel
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def signupview(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, '', password)
            return render(request, 'memoapp/signup.html')
        except IntegrityError:
            return render(request, 'memoapp/signup.html', {'error':'このユーザーはすでに登録されています。'})
    return render(request, 'memoapp/signup.html')


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
