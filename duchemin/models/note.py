from django.db import models
from django.contrib.auth.models import User
from duchemin.models.piece import DCPiece


class DCNote(models.Model):
    piece = models.ForeignKey(DCPiece, related_name="notes")
    author = models.ForeignKey(User, related_name="notes")
    time = models.DateTimeField(auto_now=True)
    text = models.TextField()

    def __unicode__(self):
        return u"{} ({} {})".format(self.piece, self.author, self.time)

    class Meta:
        app_label = "duchemin"
        verbose_name = "Note"
        verbose_name_plural = "Notes"
