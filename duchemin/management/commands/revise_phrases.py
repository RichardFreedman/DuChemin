#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.core.management.base import BaseCommand, CommandError
from duchemin.models import DCPhrase

import sys
import csv
import os


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        script_dir = os.path.dirname(__file__)
        rel_path = "revised_phrases.csv"
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path, 'rb') as csv_file:
            for line in csv.reader(csv_file):
                try:
                    if line[0]:
                        phrase = DCPhrase.objects.get(phrase_id=eval(line[0]))
                        phrase.phrase_start = line[3]
                        phrase.phrase_stop = line[4]
                        phrase.rhyme = line[5]
                        phrase.phrase_text = line[6]
                        phrase.save()
                except:
                    e = str(sys.exc_info())
                    self.stdout.write('%s\n' % e, ending='')
