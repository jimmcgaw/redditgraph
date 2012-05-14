from django.conf.urls.defaults import *

urlpatterns = patterns('redditgraph.views',
  url(r'^$', 'index', name='index'),
  url(r'^recommended/$', 'recommended', name='recommended'),
  url(r'^recommended/(?P<username>[-\w]+)/links/$', 'get_recommended_links', name='user_recommended_links'),
  url(r'^graph_json/$', 'graph_json', name='graph_json'),
)