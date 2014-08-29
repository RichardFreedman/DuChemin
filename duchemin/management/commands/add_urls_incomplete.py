from django.core.management.base import BaseCommand
from duchemin.models import DCPiece
from optparse import make_option

import sys


class Command(BaseCommand):
    help = "Fills in the PDF urls for the incomplete pieces"

    option_list = BaseCommand.option_list + (
        make_option(
            '--dev',
            action='store_true',
            dest='dev',
            default=False,
            help='Use dev URL instead of production URL',
            ),
    )

    def handle(self, *args, **options):
        if options.get('dev', False):
            PATH = 'http://duchemin-dev.haverford.edu/'
        else:
            PATH = 'http://digitalduchemin.org/'
        MEI_PATH = PATH + 'mei/'
        MP3_PATH = PATH + 'audio/'
        PDF_PATH = PATH + 'pdf/'
        for piece in DCPiece.objects.all():
            try:
                if ('DC12' in piece.piece_id or
                        'DC13' in piece.piece_id or
                        'DC14' in piece.piece_id or
                        'DC15' in piece.piece_id or
                        'DC16' in piece.piece_id):
                    piece.pdf_link = PDF_PATH + piece.piece_id + '.pdf'
                piece.save()
            except:
                e = str(sys.exc_info())
                self.stdout.write('%s\n' % e, ending='')
