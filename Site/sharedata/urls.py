from django.urls import path
from . import views 
from django.conf.urls import url

urlpatterns = [
    path('<str:userprofile>/', views.sharedata, name="sharedata"),
    path('playlist/<int:year>/<str:month>/<str:userprofile>/', views.shareplaylist, name="shareplaylist"),
    path('songs/<str:userprofile>/', views.sharesong, name="sharesong"),
    path('artists/<str:userprofile>/', views.shareartist, name="shareartist"),
]