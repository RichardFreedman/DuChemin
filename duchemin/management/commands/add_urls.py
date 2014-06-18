from django.core.management.base import BaseCommand, CommandError
from duchemin.models import DCPiece

import sys

class Command(BaseCommand):
    help = "Fills in the MEI and audio urls"

    def handle(self, *args, **kwargs):
        MEI_PATH = 'http://duchemin-dev.haverford.edu/mei/'
        MP3_PATH = 'http://duchemin-dev.haverford.edu/audio/'
        for piece in DCPiece.objects.all():
            try:
                piece.mei_link = MEI_PATH + piece.piece_id + '.xml'
                piece.audio_link = MP3_PATH + piece.piece_id + '.mp3'
                piece.save()
            except:
            	e = str(sys.exc_info())
                self.stdout.write('%s\n' % e, ending='')

