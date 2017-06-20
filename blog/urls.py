"""djangomp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),

    url(r'^req/$', views.req, name='req'),

    url(r'^shows/$', views.shows, name='shows'),

    url(r'^logout/$', views.signout, name='signout'),

    url(r'^upload_pic/$', views.upload_pic, name='upload_pic'),

    url(r'^signup/$', views.signup, name='signup'),

    url(r'^home/$', views.home, name='home'),

    url(r'^myPosts/$', views.myPosts, name='myPosts'),

    url(r'^search/$', views.search, name='search'),

    url(r'^(?P<Post_id>[0-9]+)/$', views.details, name='detail'),

    url(r'^(?P<Post_id>[0-9]+)/updates/$', views.updates, name='updates'),

    url(r'^(?P<Post_id>[0-9]+)/updates/updatefin$', views.updatefin, name='updatefin'),

    url(r'^(?P<Post_id>[0-9]+)/delete/$', views.delete, name='delete'),

    url(r'^post/$', views.newPost, name='newPost'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
