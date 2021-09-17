from django.urls import path
from django.urls.conf import include
from memoapp import views

urlpatterns = [
    path('signup/', views.signupview, name='signup'),
    path('signin/', views.signinview, name='signin'),
    path('signout/', views.signoutview, name='signout'),
    path('list/', views.listview, name='list'),
    path('detail/<int:pk>', views.detailview, name='detail'),
    path('create/', views.createview, name='create'),
    path('edit/<int:pk>', views.editview, name='edit'),
]
