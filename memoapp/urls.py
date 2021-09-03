from django.urls import path
from django.urls.conf import include
from memoapp import views

urlpatterns = [
    path('signup/', views.signupview, name='signup'),
    path('signin/', views.signinview, name='signin'),
    path('signout/', views.signoutview, name='signout'),
    path('list/', views.listview, name='list'),
    path('create/', views.createview, name='create'),
    path('edit/', views.editview, name='edit'),
]
