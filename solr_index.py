#!/usr/bin/env python
import os
import sys
import solr
import uuid


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "duchemin.settings")
    from duchemin.models.analysis import DCAnalysis
    from duchemin.models.book import DCBook
    from duchemin.models.piece import DCPiece
    from django.conf import settings

    print "Using: {0}".format(settings.SOLR_SERVER)
    solrconn = solr.SolrConnection(settings.SOLR_SERVER)

    books = DCBook.objects.all()
    all_books = []
    print "Adding books"
    for book in books:
        d = {
            'type': 'duchemin_book',
            'id': str(uuid.uuid4()),
            'book_id': int(book.book_id),
            'book_title': book.title,
        }
        all_books.append(d)
    solrconn.add_many(all_books)
    solrconn.commit()
    print "Done adding books"

    pieces = DCPiece.objects.all()
    all_pieces = []
    for piece in pieces:
        # fix the composer name
        composer_name = ""
        if piece.composer_id.given_name != "":
            composer_name = u"{0}, {1}".format(piece.composer_id.surname, piece.composer_id.given_name)
        else:
            composer_name = u"{0}".format(piece.composer_id.surname)

        d = {
            'type': 'duchemin_piece',
            'id': str(uuid.uuid4()),
            'piece_id': piece.piece_id,
            'book_title': piece.book_id.title,
            'book_id': int(piece.book_id.book_id),
            'book_id_title': "{0}_{1}".format(piece.book_id.book_id, piece.book_id.title),
            'title': piece.title,
            'composer': composer_name,
            'pdf_link': piece.pdf_link,
            'mei_link': piece.mei_link,
            'audio_link': piece.audio_link,
        }

        all_pieces.append(d)
    solrconn.add_many(all_pieces)
    solrconn.commit()
    print "Done adding pieces"

    analyses = DCAnalysis.objects.all()
    for i, analysis in enumerate(analyses):
        piece = analysis.composition_number
        composer = analysis.composition_number.composer_id
        composer_name = ""
        if composer.given_name != "":
            composer_name = u"{0}, {1}".format(composer.surname, composer.given_name)
        else:
            composer_name = u"{0}".format(composer.surname)

        contributor_name = ""
        if analysis.analyst.given_name != "":
            contributor_name = u"{0}, {1}".format(analysis.analyst.surname, analysis.analyst.given_name)
        else:
            contributor_name = u"{0}".format(analysis.analyst.surname)

        if analysis.cadence == "Yes":
            cadence = True
        else:
            cadence = False

        if analysis.cadence_alter:
            cadence_alter = [x.strip() for x in analysis.cadence_alter.split(",")]
        else:
            cadence_alter = None

        if analysis.other_contrapuntal:
            other_counterpoint = [x.strip() for x in analysis.other_contrapuntal.split(",")]
        else:
            other_counterpoint = None

        d = {
            'type': 'duchemin_analysis',
            'id': str(uuid.uuid4()),
            'analysis_id': analysis.id,
            'contributor': contributor_name,
            'piece_id': analysis.composition_number.piece_id,
            'title': analysis.composition_number.title,
            'composer': composer_name,
            'book_title': analysis.composition_number.book_id.title,
            'book_id': piece.book_id.book_id,
            'book_id_title': "{0}_{1}".format(piece.book_id.book_id, piece.book_id.title),
            'phrase_number': analysis.phrase_number.phrase_num,
            'start_measure': analysis.start_measure,
            'stop_measure': analysis.stop_measure,
            'is_cadence': cadence,
            'cadence_kind': analysis.cadence_kind,
            'cadence_alter': cadence_alter,
            'cadence_role_cantz': analysis.cadence_role_cantz,
            'cadence_role_tenz': analysis.cadence_role_tenz,
            'cadence_final_tone': analysis.cadence_final_tone,
            'voices_p6_up': analysis.voices_p6_up,
            'voices_p6_lo': analysis.voices_p6_lo,
            'voices_p3_up': analysis.voices_p3_up,
            'voices_p3_lo': analysis.voices_p3_lo,
            'voices_53_up': analysis.voices_53_up,
            'voices_53_lo': analysis.voices_53_lo,
            'other_formulas': analysis.other_formulas,
            'other_pres_type': analysis.other_pres_type,
            'voice_role_up1_nim': analysis.voice_role_up1_nim,
            'voice_role_lo1_nim': analysis.voice_role_lo1_nim,
            'voice_role_up2_nim': analysis.voice_role_up2_nim,
            'voice_role_lo2_nim': analysis.voice_role_lo2_nim,
            'voice_role_dux1': analysis.voice_role_dux1,
            'voice_role_com1': analysis.voice_role_com1,
            'voice_role_dux2': analysis.voice_role_dux2,
            'voice_role_com2': analysis.voice_role_com2,
            'voice_role_un_oct': analysis.voice_role_un_oct,
            'voice_role_fifth': analysis.voice_role_fifth,
            'voice_role_fourth': analysis.voice_role_fourth,
            'voice_role_above': analysis.voice_role_above,
            'voice_role_below': analysis.voice_role_below,
            'other_contrapuntal': other_counterpoint,
            'text_treatment': analysis.text_treatment,
            'repeat_kind': analysis.repeat_kind,
            'earlier_phrase': analysis.earlier_phrase,
            'comment': analysis.comment,
            'repeat_exact_varied': analysis.repeat_exact_varied
        }
        # print d
        solrconn.add(**d)
        if i % 100 == 0:
            solrconn.commit()
    solrconn.commit()
    print "Done adding analyses"

    sys.exit()
