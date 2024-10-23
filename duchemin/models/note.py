from django.db import models
from django.contrib.auth.models import User
from duchemin.models.piece import DCPiece


class DCNote(models.Model):
    piece = models.ForeignKey("duchemin.DCPiece", on_delete=models.CASCADE, related_name="notes")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    text = models.TextField()

    def __unicode__(self):
        return u"{0} ({1})".format(self.piece, self.author)

    class Meta:
        app_label = "duchemin"
        verbose_name = "Note"
        verbose_name_plural = "Notes"
