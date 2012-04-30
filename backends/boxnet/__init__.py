import os
import base64
import urllib2

from django.conf import settings
from backends.boxnet.models import BoxnetSource

from backends.boxnet.boxdotnet import BoxDotNet
boxnet = BoxDotNet()

BOXNET_API_BASE_URL = 'https://www.box.net/api/1.0/'

class BoxnetWrapper:
    @staticmethod
    def get_resource(source, resource_id):
        try:
            obj = BoxnetSource.objects.get(source=source)
        except BoxnetSource.DoesNotExist:
            # source path does not exist
            return {'error' : 'Source not found'}
        # didn't find better way to find out if resource belongs to a folder through Boxnet API
        default_args = {'api_key': settings.BOXNET_APIKEY, 
                       'auth_token': settings.BOXNET_AUTH_TOKEN}
        data = { 'folder_id': obj.folder_id, 'params':['nozip',] }
        data.update(default_args)
        ret_data = boxnet.get_account_tree(**data)
        if not search_file(ret_data.tree[0].folder[0], resource_id):
            return {'error' : 'Resource not found'}

        # the only way to get file contents - download
        resource_url = '%sdownload/%s/%s' % (
            BOXNET_API_BASE_URL, settings.BOXNET_AUTH_TOKEN, resource_id
            )
        try:
            response = urllib2.urlopen(resource_url)
        except:
            return {'error' : 'Resource not found'}
        else:
            return {
                'contents' : base64.b64encode(response.read())
            }

    @staticmethod
    def list_resources(source, tags):
        default_args = {'api_key': settings.BOXNET_APIKEY, 
                       'auth_token': settings.BOXNET_AUTH_TOKEN}
        ret_list = []
        try:
            obj = BoxnetSource.objects.get(source=source)
        except BoxnetSource.DoesNotExist:
            # source path does not exist
            return {'error' : 'Source not found'}
        data = { 'folder_id': obj.folder_id, 'params':['nozip',] }
        data.update(default_args)
        ret_data = boxnet.get_account_tree(**data)
        if tags:
            return search_tags(ret_data.tree[0].folder[0], tags)
        else:
            return get_all_files(ret_data.tree[0].folder[0])

def search_tags(folder_node, tag_list, initial_list=None):
    ret_list = []
    initial_list = initial_list or []
    try:
        for fld in folder_node.folders[0].folder:
            new_list = list(tag_list)
            if fld['name'] in new_list:
                new_list.remove(fld['name'])
            new_tags_list = list(initial_list)
            new_tags_list.append(fld['name'])
            if new_list:
                ret_list += search_tags(fld, new_list, new_tags_list)
            else:
                ret_list += get_all_files(fld, new_tags_list)
    except:
        pass

    return ret_list
    
def get_all_files(folder_node, initial_list=None):
    initial_list = initial_list or []
    ret_list = []
    try:
        for f in folder_node.files[0].file:
            f_split = f['file_name'].split('.')
            ext = '' if not len(f_split)>1 else f_split[-1]
                
            ret_list.append({
                    'name' : f['file_name'],
                    'resource_id' : f['id'],
                    'tags' : initial_list, 
                    'type' : ext,
                    'size' : f['size']
                    })
    except:
        pass

    try:
        for fld in folder_node.folders[0].folder:
            new_list = list(initial_list)
            new_list.append(fld['name'])
            ret_list += get_all_files(fld, new_list)
    except:
        pass

    return ret_list
    

def search_file(folder_node, resource_id):
    """
        Searches file recursively in a folder
    """
    try:
        for f in folder_node.files[0].file:
            if f['id'] == resource_id:
                return True
    except:
        pass

    try:
        for fld in folder_node.folders[0].folder:
            if search_file(fld, resource_id):
                return True
    except:
        pass
        
    return False
