from django.contrib import admin

from backends.filesystem.models import SourcePath

admin.site.register(SourcePath)
