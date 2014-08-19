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
                if ('DC01' in piece.piece_id or
                        'DC02' in piece.piece_id or
                        'DC03' in piece.piece_id or
                        'DC04' in piece.piece_id or
                        'DC05' in piece.piece_id or
                        'DC06' in piece.piece_id or
                        'DC07' in piece.piece_id or
                        'DC08' in piece.piece_id or
                        'DC09' in piece.piece_id or
                        'DC10' in piece.piece_id or
                        'DC11' in piece.piece_id):
                    piece.audio_link = MP3_PATH + piece.piece_id + '.mp3'
                piece.save()
            except:
                e = str(sys.exc_info())
                self.stdout.write('%s\n' % e, ending='')
