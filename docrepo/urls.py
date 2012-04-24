from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('docrepo.views',
    url(r'^list/(?P<source_name>[\w_]+)/$', 'get_list'),
)
