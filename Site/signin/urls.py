from . import views 
from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('', views.signin, name="signin"),
    path('logout/', views.signout, name="signout"),
]
