"""source URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'source.views.home', name = "home"),
    url(r'^login/$', 'source.views.login', name ="login"),
    url(r'^signedout/$', 'app.views.sign_out', name='signout'),

    url(r'^get_layer_ID_token/$', 'layer_handlers.views.get_identity_token', name='getlayerID'),

    url(r'^init_login_data_store/$', 'layer_handlers.views.save_login_data', name='save_login_data'),
    url(r'^first_login/', 'app.views.first_login', name='first_login'),
    url(r'^initial_setup/$', 'app.views.setup', name='setup'),

    url(r'^app/$', 'app.views.home', name='app_home'),
    url(r'^app/init_convo/$', 'layer_handlers.views.new_convo', name='newconvo'),
    url(r'^app/join_convo/$', 'layer_handlers.views.join_convo', name = 'joinconvo'),
    url(r'^app/convo/', 'app.views.convo', name ='convo'), 
    
    url(r'^app/support/qpdiogtqerfsdfrwde134sf/$', 'app.views.id_to_name', name ='idtoname'),
    url(r'^goaway/$', 'source.views.goaway', name='goaway'),
    url(r'^convo_get/$', 'layer_handlers.views.displayConvo', name='get_convo'),
]
