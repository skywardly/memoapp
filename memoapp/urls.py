from django.urls import path
from django.urls.conf import include
from memoapp import views

urlpatterns = [
    path('signup/', views.signupview),
    path('signin/', views.signinview),
]
