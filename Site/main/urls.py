from django.urls import path
from . import views 
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name="home"),
    path('playlist/<int:year>/<str:month>/', views.playlist, name="playlist"),
]
#playlist/<int:year>/<str:month>/