import os
from django.db import models


class DCFile(models.Model):
    class Meta:
        app_label = "duchemin"
        verbose_name = "File"
        verbose_name_plural = "Files"

    description = models.CharField(max_length=255, blank=True)
    attachment = models.FileField(upload_to=os.path.join("%Y", "%m", "%d"))

    def __unicode__(self):
        return u"{0} ({1})".format(self.attachment.name, self.attachment.size)
