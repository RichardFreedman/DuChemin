from django.core.management.base import BaseCommand, CommandError
from duchemin.models import DCAnalysis

import sys


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for analysis in DCAnalysis.objects.all():
            try:
                if analysis.repeat_kind == '':
                    analysis.repeat_kind = None
                    analysis.save()
            except:
                e = str(sys.exc_info())
                self.stdout.write('%s\n' % e, ending='')
