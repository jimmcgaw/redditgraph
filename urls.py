from django.conf.urls.defaults import * 
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('', 
    url(r'^', include('redditgraph.urls')),
    #Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    #Static Links
#    url(r'^', TemplateView.as_view(template_name='home.html'), name='home'),
    
)

#urlpatterns += patterns('redditgraph_site.redditgraph.views',
#   url(r'^redditgraph/$', 'redditgraph_view', name='redditgraph'),
#)


if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns

