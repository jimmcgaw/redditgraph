from django.conf.urls.defaults import *

urlpatterns = patterns('redditgraph.views',
  url(r'^$', 'index', name='index'),
  url(r'^graph_json/$', 'graph_json', name='graph_json'),
)