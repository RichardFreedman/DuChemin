from django.db import models
from duchemin.models.piece import DCPiece
from duchemin.models.person import DCPerson
from duchemin.models.file import DCFile


class DCReconstruction(models.Model):
    class Meta:
        app_label = "duchemin"
        verbose_name = "Reconstruction"
        verbose_name_plural = "Reconstructions"

    piece = models.ForeignKey(DCPiece, on_delete=models.CASCADE, to_field="piece_id")
    reconstructor = models.ForeignKey(DCPerson, on_delete=models.CASCADE, to_field="person_id")
    attachments = models.ManyToManyField(DCFile)

    def __unicode__(self):
        return self.recon_id

    @property
    def recon_id(self):
        return u"{0}_{1}".format(self.piece.piece_id, self.reconstructor.surname)

    @property
    def recon_filename(self):
        return u"{0}_{1}.xml".format(self.piece.piece_id, self.reconstructor.surname)
