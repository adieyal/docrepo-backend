from backends.filesystem import FileSystem
from backends.filesystem.constants import BACKEND_ID as FS_BACKEND_ID

BACKEND_ID_MAP = {
    FS_BACKEND_ID : FileSystem,
}

class Backend:
    """
        Backend abstraction class for docrepo application
    """
    def __init__(self, backend_id):
        self._class = BACKEND_ID_MAP[backend_id]

    def list_resources(self, source, *tags):
        return self._class.list_resources(source, *tags)

