import os
import base64

from backends.filesystem.models import SourcePath

class FileSystem:

    @staticmethod
    def get_resource(source, relpath):
        try:
            obj = SourcePath.objects.get(source=source)
        except SourcePath.DoesNotExist:
            # source path does not exist
            return {'error' : 'Source not found'}
        source_path = os.path.normpath(obj.path)
        if not os.path.exists(source_path):
            # no such directory
            return {'error' : 'Source not found'}

        fullpath = source_path + relpath
        if not os.path.exists(fullpath):
            return {'error' : 'Resource not found'}

        f = open(fullpath)
        return {
            "contents" : base64.b64encode(f.read())
        }
        
    @staticmethod
    def list_resources(source, tags):
        ret_list = []
        try:
            obj = SourcePath.objects.get(source=source)
        except SourcePath.DoesNotExist:
            # source path does not exist
            return {'error' : 'Source not found'}
        source_path = os.path.normpath(obj.path)
        if not os.path.exists(source_path):
            # no such directory
            return {'error' : 'Source not found'}
            
        if tags:
            for root, dirs, files in os.walk(source_path):
                cur_path = root
                subdirs = list(tags)
                pathlist = []

                # get all relative subdirs until we reach the source path
                # since each directory is considered to be a tag
                # check each directory to evaluate whether this path matches the query
                while cur_path != source_path:
                    cur_path, tail = os.path.split(cur_path)
                    if tail:
                        # make a list of tags(subdirs)
                        pathlist.insert(0, tail)
                        if tail in subdirs:
                            # one of tags(subdirs) is found!
                            # remove it from list and continue searching
                            subdirs.remove(tail)

                if not subdirs:
                    # all subdirs were found in the current root
                    # this means that all the files in the root directory (recursively)
                    # match the given query
                    ret_list.extend(get_all_files(root, pathlist))
                    # no need to get into subdirs of root
                    dirs = []
        else:
            # get all files recursively
            ret_list = get_all_files(source_path)
            
        for resource in ret_list:
            fullpath = resource["fullpath"]
            del resource["fullpath"]
            resource["resource_id"] = fullpath.replace(source_path, "")
        return ret_list

def get_all_files(path, initial_list=None):
    initial_list = initial_list or []

    insert_pos = len(initial_list)
    ret_list = []
    for root, dirs, files in os.walk(path):
        cur_path = root
        pathlist = list(initial_list)
        while cur_path != path:
            cur_path, tail = os.path.split(cur_path)
            if tail:
                pathlist.insert(insert_pos, tail)

        for f in files:
            # get all required data for a file to return
            fullpath = os.path.join(root, f)
            basename, extension = os.path.splitext(fullpath)
            if len(extension) > 0:
                extension = extension[1:]
            size = os.path.getsize(fullpath)

            ret_list.append({
                'name' : f, 
                'size' : size, 
                'type' : extension, 
                'tags' : pathlist,
                'fullpath' : fullpath
            })

    return ret_list
