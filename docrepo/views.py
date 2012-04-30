from django.http import HttpResponse
from django.utils import simplejson

from docrepo.models import Source
from backends import Backend
from django.http import Http404

def get_list(request, source_name):
    """
        Returns json encoded list of resources for a given source_name.
        Optionally accepts tags list as a request parameter
    """
    tags = request.GET.get('tags', None)
    if tags:
        # make a list of tags
        tags = tags.strip().split(" ")
    try:
        source = Source.objects.get(name=source_name)
    except Source.DoesNotExist:
        response_data = {'error': 'Source not found'}
    else:
        response_data = Backend(source.backend_id).list_resources(source, tags)

    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

def get_resource(request, source_name):
    """
        Returns a binary64 stream containing the contents of the file. 
    """

    resource_id = request.GET.get('resource_id', None)
    if not resource_id:
        raise Http404

    try:
        source = Source.objects.get(name=source_name)
    except Source.DoesNotExist:
        response_data = {'error': 'Source not found'}
    else:
        response_data = Backend(source.backend_id).get_resource(source, resource_id)

    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
