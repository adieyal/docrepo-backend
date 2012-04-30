from django.db import models
from django.conf import settings

from docrepo.models import Source

class BoxnetSource(models.Model):
    source = models.OneToOneField(Source, 
                    limit_choices_to = {
                        'backend_id__in': [settings.BOXNET_BACKEND_ID, settings.BOXNET2_BACKEND_ID] 
                    })
    folder_id = models.CharField(max_length=50)

    def __unicode__(self):
        return self.source.name
