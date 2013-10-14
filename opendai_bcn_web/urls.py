from django.conf.urls import patterns, url
from opendai_bcn_web import views
from opendai_bcn_web.data_cron import DataCron


#from djgeojson.views import GeoJSONLayerView
#from opendai_bcn_web.views import TestGeoLayer
#from opendai_bcn_web.models import TestGeo

#===============================================================================
# urlpatterns = patterns('django.views.generic.simple',
#    (r'^foo/$',             'direct_to_template', {'template': 'foo_index.html'}),
#    (r'^foo/(?P<id>\d+)/$', 'direct_to_template', {'template': 'foo_detail.html'}),
# )
#===============================================================================

# init
c = DataCron () 
#c.get_pollution()

urlpatterns = patterns('',
    
    url(r'^$', views.index),
    url(r'^bcn.geojson$', views.bcn_geojson, name='data'),
    
    #url(r'^data.geojson$', TestGeoLayer.as_view(model=TestGeo), name='data'),
    
 )

