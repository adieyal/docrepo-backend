from django.db import models

from backends.constants import BACKEND_IDS

class Source(models.Model):
    name = models.CharField(max_length=200, unique=True)
    backend_id = models.CharField(max_length=30, choices=BACKEND_IDS)

    def __unicode__(self):
        return self.name

