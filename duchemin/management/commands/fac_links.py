from django.core.management.base import BaseCommand, CommandError
from duchemin.models import DCBook

import sys


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        codes = { 1: '149',   2: '140',   3: '141',   4: '142',
                  5: '151',   6: '152',   7: '153',   8: '154',
                  9: '165',  10: '170',  11: '193',  12: '228',
                 13: '229',  14: '261',  15: '262',  16: '323',
                 }
        for book in DCBook.objects.all():
            try:
                if book.book_id and book.book_id >= 1 and book.book_id <= 16:
                    book.cesr = ('http://ricercar-old.cesr.univ-tours.fr/3-programmes/EMN/duchemin/pages/consult.asp?table=A' +
                                 codes[book.book_id]
                                 )
                    book.save()
                else:
                    self.stdout.write(str(book.book_id) + '\n', ending='')
            except:
                e = str(sys.exc_info())
                self.stdout.write('%s\n' % e, ending='')
