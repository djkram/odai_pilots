from django.conf.urls import patterns, url

from opendai_lleida_web import views
#===============================================================================
# urlpatterns = patterns('django.views.generic.simple',
#    (r'^foo/$',             'direct_to_template', {'template': 'foo_index.html'}),
#    (r'^foo/(?P<id>\d+)/$', 'direct_to_template', {'template': 'foo_detail.html'}),
# )
#===============================================================================

# init


urlpatterns = patterns('',
    
    url(r'^$', views.index),
    url(r'^alert/all$', views.alerts),
    url(r'^alert/(\d+)/$', views.alerts_by_day),
    url(r'^buslines.geojson$', views.buslines_lines_geojson),
    url(r'^bustop/all$', views.bustops_all),
    url(r'^bustop/near$', views.bustops_near),
    url(r'^bustop/(\d+)/$', views.bustops_by_id),
    url(r'^pois/category/all$', views.pois_category_all),
    url(r'^pois/(\d+)/$', views.pois_by_category_id),
    url(r'^accessibility/all$', views.accessibility_all),
    url(r'^accessibility/(\d+)/$', views.accessibility_id),
    url(r'^accessibility/category/(\d+)/$', views.accessibility_category_id),
    url(r'^accessibility/feature/(\d+)/$', views.accessibility_feature_id),
    url(r'^accessibility/level/(\d+)/$', views.accessibility_level_id),
    
 )

