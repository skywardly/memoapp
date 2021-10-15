from memoapp.models import MemoModel, MyUser
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from memoapp.forms import LoginForm, MemoForm

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
            message = 'ログインしました。'
            messages.success(request, message)
            return redirect('list')
        else:
            return render(request, 'memoapp/signin.html', {})
    return render(request, 'memoapp/signin.html', {})


def signoutview(request):
    logout(request)
    return redirect('signin')


@login_required
def listview(request):
    object_list = MemoModel.objects.filter(user=request.user.id)

    """ 検索機能の処理 """
    keyword = request.GET.get('keyword')
    if keyword:
        object_list = object_list.filter(
            Q(memo__icontains=keyword)
        )
        messages.success(request, '「{}」の検索結果'.format(keyword))

    return render(request, 'memoapp/list.html', {'object_list':object_list})


@login_required
def detailview(request, pk):
    object = MemoModel.objects.filter(user=request.user.id).get(pk=pk)
    return render(request, 'memoapp/detail.html', {'object':object})


@login_required
def createview(request):
    if request.method == 'GET':
        form = MemoForm()
        return render(request, 'memoapp/edit.html', {'form': form})
    elif request.method == 'POST':
        form = MemoForm(request.POST)
        if form.is_valid():
            MemoModel.objects.create(user=request.user, memo=form.cleaned_data['memo'])
            messages.success(request, '作成しました。')
            return redirect('list')
        else:
            return render(request, 'memoapp/edit.html', {'form': form})

'''
@login_required
def createview(request):
    form = MemoForm(request.POST or None)
    if form.is_valid():
        MemoModel.objects.create(user=request.user, memo=form.cleaned_data['memo'])
        messages.success(request, '作成しました。')
        return redirect('list')
    return render(request, 'memoapp/edit.html', {'form': form})
'''


@login_required
def editview(request, pk):
    object = MemoModel.objects.get(pk=pk)
    if request.method == "POST":
        form = MemoForm(request.POST, instance=object)
        if form.is_valid():
            object = form.save(commit=False)
            object.save()
            return redirect('detail', pk=object.pk)
    else:
        form = MemoForm(instance=object)
    return render(request, 'memoapp/edit.html', {'form': form})


@require_POST
def deleteview(request, pk):
    memo = MemoModel.objects.get(pk=pk)
    memo.delete()
    return redirect('list')
