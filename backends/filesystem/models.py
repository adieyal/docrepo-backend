from django.db import models
from django.conf import settings

from docrepo.models import Source

MAX_PATH_LENGTH = 4096

class SourcePath(models.Model):
    source = models.OneToOneField(Source, 
                    limit_choices_to = {'backend_id': settings.FILESYSTEM_BACKEND_ID})
    path = models.TextField(max_length=MAX_PATH_LENGTH)

    def __unicode__(self):
        return "%s as %s" %(self.path, self.source.name)
