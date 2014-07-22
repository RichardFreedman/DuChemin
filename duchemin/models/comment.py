from django.db import models
from django.contrib.auth.models import User


class DCComment(models.Model):
    piece = models.ForeignKey("duchemin.DCPiece", related_name="comments")
    author = models.ForeignKey(User, related_name="comments")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    text = models.TextField()

    def __unicode__(self):
        return u"{0} ({1} {2})".format(self.piece, self.author, self.created)

    class Meta:
        app_label = "duchemin"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
