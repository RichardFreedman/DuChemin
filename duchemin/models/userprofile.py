from django.db import models
from django.contrib.auth.models import User
from duchemin.models.piece import DCPiece
from duchemin.models.analysis import DCAnalysis
from duchemin.models.reconstruction import DCReconstruction
from duchemin.models.person import DCPerson


class DCUserProfile(models.Model):
    class Meta:
        app_label = "duchemin"

    user = models.OneToOneField(User, db_index=True)
    favourited_piece = models.ManyToManyField(DCPiece, blank=True, db_index=True)
    favourited_analysis = models.ManyToManyField(DCAnalysis, blank=True, db_index=True)
    favourited_reconstruction = models.ManyToManyField(DCReconstruction, blank=True, db_index=True)
    person = models.ForeignKey(DCPerson, blank=True, null=True, help_text="Link this account with a DuChemin User", db_index=True, related_name="profile")

User.profile = property(lambda u: DCUserProfile.objects.get_or_create(user=u)[0])