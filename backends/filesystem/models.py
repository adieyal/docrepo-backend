from django.db import models

from docrepo.models import Source
from backends.filesystem.constants import BACKEND_ID

MAX_PATH_LENGTH = 4096
BACKEND_ID = 'filesystem'

class SourcePath(models.Model):
    source = models.OneToOneField(Source, 
                        limit_choices_to = {'backend_id': BACKEND_ID})
                        
    path = models.TextField(max_length=MAX_PATH_LENGTH)

    def __unicode__(self):
        return "%s as %s" %(self.path, self.source.name)
