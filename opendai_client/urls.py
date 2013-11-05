from django.conf.urls import patterns, url
from opendai_client import views

urlpatterns = patterns('',
    
    url(r'^$', views.geocoding),

    
 )

