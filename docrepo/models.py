from django.db import models
from django.conf import settings

class Source(models.Model):
    name = models.CharField(max_length=200, unique=True)
    backend_id = models.CharField(max_length=30, choices=settings.BACKEND_IDS)

    def __unicode__(self):
        return self.name
