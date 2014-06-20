from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from duchemin.models.person import DCPerson
from duchemin.models.piece import DCPiece
from duchemin.models.phrase import DCPhrase


class DCAnalysis(models.Model):
    class Meta:
        app_label = "duchemin"
        verbose_name = "Analysis"
        verbose_name_plural = "Analyses"

    timestamp = models.CharField(max_length=64, blank=True, null=True)
    analyst = models.ForeignKey(DCPerson, to_field='person_id', db_index=True, related_name="analyses")
    composition_number = models.ForeignKey(DCPiece, to_field='piece_id', db_index=True, related_name="pieces")
    phrase_number = models.ForeignKey(DCPhrase, to_field='phrase_id', db_index=True, related_name="phrases")
    start_measure = models.IntegerField(blank=True, null=True)
    stop_measure = models.IntegerField(blank=True, null=True)
    is_cadence = models.BooleanField()
    cadence_kind = models.CharField(max_length=64, blank=True, null=True)
    cadence_alter = models.CharField(max_length=64, blank=True, null=True)
    cadence_role_cantz = models.CharField(max_length=16, blank=True, null=True)
    cadence_role_tenz = models.CharField(max_length=16, blank=True, null=True)
    cadence_final_tone = models.CharField(max_length=16, blank=True, null=True)
    voices_p6_up = models.CharField(max_length=16, blank=True, null=True)
    voices_p6_lo = models.CharField(max_length=16, blank=True, null=True)
    voices_p3_up = models.CharField(max_length=16, blank=True, null=True)
    voices_p3_lo = models.CharField(max_length=16, blank=True, null=True)
    voices_53_up = models.CharField(max_length=16, blank=True, null=True)
    voices_53_lo = models.CharField(max_length=16, blank=True, null=True)
    other_formulas = models.CharField(max_length=64, blank=True, null=True)
    other_pres_type = models.CharField(max_length=64, blank=True, null=True)
    voice_role_up1_nim = models.CharField(max_length=16, blank=True, null=True)
    voice_role_lo1_nim = models.CharField(max_length=16, blank=True, null=True)
    voice_role_up2_nim = models.CharField(max_length=16, blank=True, null=True)
    voice_role_lo2_nim = models.CharField(max_length=16, blank=True, null=True)
    voice_role_dux1 = models.CharField(max_length=16, blank=True, null=True)
    voice_role_com1 = models.CharField(max_length=16, blank=True, null=True)
    voice_role_dux2 = models.CharField(max_length=16, blank=True, null=True)
    voice_role_com2 = models.CharField(max_length=16, blank=True, null=True)
    voice_role_un_oct = models.CharField(max_length=16, blank=True, null=True)
    voice_role_fifth = models.CharField(max_length=16, blank=True, null=True)
    voice_role_fourth = models.CharField(max_length=16, blank=True, null=True)
    voice_role_above = models.CharField(max_length=16, blank=True, null=True)
    voice_role_below = models.CharField(max_length=16, blank=True, null=True)
    other_contrapuntal = models.CharField(max_length=128, blank=True, null=True)
    text_treatment = models.CharField(max_length=128, blank=True, null=True)
    repeat_kind = models.CharField(max_length=64, blank=True, null=True)
    earlier_phrase = models.CharField(max_length=16, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    repeat_exact_varied = models.CharField(max_length=16, blank=True, null=True)

    needs_review = models.BooleanField(default=False)

    def __unicode__(self):
        return u"{0}".format(self.id)


@receiver(post_save, sender=DCAnalysis)
def solr_index(sender, instance, created, **kwargs):
    print "Indexing in solr"
    import uuid
    from django.conf import settings
    import solr

    solrconn = solr.SolrConnection(settings.SOLR_SERVER)
    record = solrconn.query("analysis_id:{0}".format(instance.id))
    if record:
        # the record already exists, so we'll remove it first.
        print "Deleting ".format(record.results[0]['id'])
        solrconn.delete(record.results[0]['id'])

    # make it clear what we're working with...
    analysis = instance

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
        'is_cadence': analysis.is_cadence,
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
    solrconn.commit()


@receiver(post_delete, sender=DCAnalysis)
def solr_delete(sender, instance, **kwargs):
    from django.conf import settings
    import solr

    solrconn = solr.SolrConnection(settings.SOLR_SERVER)
    record = solrconn.query("analysis_id:{0}".format(instance.id))
    if record:
        # the record already exists, so we'll remove it first.
        print "Deleting ".format(record.results[0]['id'])
        solrconn.delete(record.results[0]['id'])

    # def __unicode__(self):
    #     return u"{0}, {1}, {2}".format(self.id, self.analyst, self.composition_number)
