from django.conf.urls import patterns, url

from opendai_lleida_web import views
from opendai_client import views as views_geo
#===============================================================================
# urlpatterns = patterns('django.views.generic.simple',
#    (r'^foo/$',             'direct_to_template', {'template': 'foo_index.html'}),
#    (r'^foo/(?P<id>\d+)/$', 'direct_to_template', {'template': 'foo_detail.html'}),
# )
#===============================================================================

# init


urlpatterns = patterns('',
    
    url(r'^$', views.index),
    url(r'^api/alert/all$', views.alerts),
    url(r'^api/alert/(\d+)$', views.alerts_by_day),
    url(r'^api/buslines.geojson$', views.buslines_lines_geojson),
    url(r'^api/buslines/all$', views.buslines_all),
    url(r'^api/buslines/(L\d+)$', views.buslines_by_id),
    url(r'^api/bustop/all$', views.bustops_all),
    url(r'^api/bustop/near$', views.bustops_near),
    url(r'^api/bustop/(\d+)$', views.bustops_by_id),
    url(r'^api/pois/category/all$', views.pois_category_all),
    url(r'^api/pois/(\d+)$', views.pois_by_category_id),
    url(r'^api/accessibility/all$', views.accessibility_all),
    url(r'^api/accessibility/(\d+)$', views.accessibility_id),
    url(r'^api/accessibility/category/all$', views.accessibility_category_all),
    url(r'^api/accessibility/category/(\d+)$', views.accessibility_category_id),
    url(r'^api/accessibility/feature/all$', views.accessibility_feature_all),
    url(r'^api/accessibility/feature/(\d+)$', views.accessibility_feature_id),
    url(r'^api/accessibility/level/(\d+)$', views.accessibility_level_id),
    url(r'^geo$', views_geo.geocoding),
    
 )

