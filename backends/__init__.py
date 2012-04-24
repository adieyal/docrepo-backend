from django.conf import settings

class Backend:
    """
        Backend abstraction class for docrepo application
    """
    def __init__(self, backend_id):
            self._class = eval(settings.BACKEND_ID_MAP[backend_id])

    def list_resources(self, source, *tags):
        return self._class.list_resources(source, *tags)

    def get_resource(self, source, resource_id):
        return self._class.get_resource(source, resource_id)

