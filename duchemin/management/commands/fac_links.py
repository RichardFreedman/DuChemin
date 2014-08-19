from django.core.management.base import BaseCommand, CommandError
from duchemin.models import DCBook

import sys


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for book in DCBook.objects.all():
            try:
                if book.book_id == 1:
                    book.cesr = 'http://ricercar.cesr.univ-tours.fr/3-programmes/EMN/duchemin/pages/consult.asp?table=A149'
                    book.save()
                else:
                    self.stdout.write(str(book.book_id) + '\n', ending='')
            except:
                e = str(sys.exc_info())
                self.stdout.write('%s\n' % e, ending='')
