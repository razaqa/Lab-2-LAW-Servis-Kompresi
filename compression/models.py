from django.db import models
from django.utils import timezone
import os
import sys

def file_path(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000

    return f"{now:%Y%m%d%H%M%S}{milliseconds}{extension}"

class File(models.Model):
    file = models.FileField(upload_to=file_path)

    def __str__(self):
        return file_path(self, self.file.name)