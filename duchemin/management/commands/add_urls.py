from django.core.management.base import BaseCommand
from duchemin.models import DCPiece
from optparse import make_option

import sys


class Command(BaseCommand):
    help = "Fills in the MEI and audio urls"

    def handle(self, *args, **options):
        MEI_PATH = '/mei/'
        MP3_PATH = '/audio/'
        for piece in DCPiece.objects.all():
            print("Processing {0}".format(piece.piece_id))
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
