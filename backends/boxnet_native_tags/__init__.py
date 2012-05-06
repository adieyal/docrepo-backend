import os

from django.conf import settings
from backends.boxnet.models import BoxnetSource
from backends.boxnet import BoxnetWrapper

from backends.boxnet.boxdotnet import BoxDotNet
boxnet = BoxDotNet()

class BoxnetNativeTags:
    @staticmethod
    def get_resource(source, resource_id):
        return BoxnetWrapper.get_resource(source, resource_id)

    @staticmethod
    def get_resource_content(source, resource_id):
        return BoxnetWrapper.get_resource_content(source, resource_id)

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
        data = { 'folder_id': obj.folder_id, 'params':['nozip', 'show_tag_names'] }
        data.update(default_args)
        ret_data = boxnet.get_account_tree(**data)
        return search_native_tags(ret_data.tree[0].folder[0], tags)

def search_native_tags(folder_node, tag_list):
    tag_list = tag_list or []
    ret_list = []
    try:
        for f in folder_node.files[0].file:
            file_tag_list = []
            search_list = list(tag_list)
            try:
                for t in f.tags[0].tag:
                    if t['name'] in search_list:
                        search_list.remove(t['name'])
                    file_tag_list.append(t['name'])
            except:
                pass
            if not search_list: # all tags were found
                f_split = f['file_name'].split('.')
                ext = '' if not len(f_split)>1 else f_split[-1]
                    
                ret_list.append({
                        'name' : f['file_name'],
                        'resource_id' : f['id'],
                        'tags' : file_tag_list, 
                        'type' : ext,
                        'size' : f['size']
                        })
    except:
        pass

    try:
        for fld in folder_node.folders[0].folder:
            ret_list += search_native_tags(fld, tag_list)
    except:
        pass

    return ret_list