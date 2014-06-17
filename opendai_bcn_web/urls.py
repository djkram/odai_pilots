from django.conf.urls import patterns, url
from opendai_bcn_web import views

from opendai_bcn_web.bcn_jobs import pollution_job

import threading

#from djgeojson.views import GeoJSONLayerView
#from opendai_bcn_web.views import TestGeoLayer
#from opendai_bcn_web.models import TestGeo

#===============================================================================
# urlpatterns = patterns('django.views.generic.simple',
#    (r'^foo/$',             'direct_to_template', {'template': 'foo_index.html'}),
#    (r'^foo/(?P<id>\d+)/$', 'direct_to_template', {'template': 'foo_detail.html'}),
# )
#===============================================================================

# init Threads
#c = DataLoad () 

#thread = threading.Thread(target=pollution_job.get_pollution)
#thread.setDaemon(True)
#thread.start()

#thread = DataLoad(my_id=1234)
#thread.start() 

urlpatterns = patterns('',
    
    url(r'^$', views.index),
    url(r'^pollution.geojson$', views.pollution_geojson),
    url(r'^pollution_async.geojson$', views.pollution_geojson_async),
    url(r'^pollution_historic$', views.pollution_historic),
    url(r'^pollution_days$', views.pollution_days),
    url(r'^weather$', views.weather_all),
    url(r'^traffic.geojson', views.traffic_lines_geojson),
    url(r'^traffic_async.geojson', views.traffic_lines_geojson_async),
    url(r'^traffic_days$', views.traffic_days),
    
    #url(r'^data.geojson$', TestGeoLayer.as_view(model=TestGeo), name='data'),
    
 )

