from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'opendai_lleida_web.views.home', name='home'),
    # url(r'^opendai_lleida_web/', include('opendai_lleida_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
        # Views
    url(r'^lleida/', include('opendai_lleida_web.urls')),
    
    # Actions
    url(r'^bcn/', include('opendai_bcn_web.urls')),
    
    

)
