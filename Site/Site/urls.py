from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', include("signup.urls"), name='signup'),
    path("signin/", views.signin, name="signin"),
    path('signout/',views.signout, name="signout"),
    path('', include("main.urls"), name="home"),
    path('home/', include("main.urls"), name="home"),
    path('home/', include("main.urls"), name="playlist"),
    path('songs/', include("songs.urls"), name="songs"),
    path('update/', include("update.urls"), name="update"),
    path('artists/', include("artists.urls"), name="artists"),
    path('', include("sharedata.urls"), name="sharedata"),
    path('', include("sharedata.urls"), name="shareplaylist"),
    path('', include("sharedata.urls"), name="sharesong"),
    path('', include("sharedata.urls"), name="shareartist"),
    #path('', include("django.contrib.auth.urls")),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)