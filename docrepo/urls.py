from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('docrepo.views',
    url(r'^list/(?P<source_name>[\w_]+)/$', 'get_list'),
    url(r'^get/(?P<source_name>[\w_]+)/$', 'get_resource'),
    url(r'^getcontent/(?P<source_name>[\w_]+)/$', 'get_resource_content', name="get_content"),
)
