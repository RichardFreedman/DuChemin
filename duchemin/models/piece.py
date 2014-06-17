from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from duchemin.models.book import DCBook
from duchemin.models.person import DCPerson
from duchemin.models.file import DCFile


class DCPiece(models.Model):
    class Meta:
        app_label = "duchemin"
        verbose_name = "Piece"
        verbose_name_plural = "Pieces"

    piece_id = models.CharField(max_length=16, unique=True, db_index=True)
    book_id = models.ForeignKey(DCBook, to_field='book_id')
    book_position = models.IntegerField(max_length=16, blank=True, null=True)
    title = models.CharField(max_length=64, blank=True, null=True)
    composer_id = models.ForeignKey(DCPerson, to_field='person_id')
    composer_src = models.CharField(max_length=64, blank=True, null=True)
    forces = models.CharField(max_length=16, blank=True, null=True)
    print_concordances = models.CharField(max_length=128, blank=True, null=True)
    ms_concordances = models.CharField(max_length=128, blank=True, null=True)
    pdf_link = models.CharField(max_length=255, blank=True, null=True)
    mei_link = models.CharField(max_length=255, blank=True, null=True)
    audio_link = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u"{0}".format(self.title)


@receiver(post_save, sender=DCPiece)
def solr_index(sender, instance, created, **kwargs):
    import uuid
    from django.conf import settings
    import solr

    solrconn = solr.SolrConnection(settings.SOLR_SERVER)
    record = solrconn.query("type:duchemin_piece piece_id:{0}".format(instance.id))
    if record:
        # the record already exists, so we'll remove it first.
        solrconn.delete(record.results[0]['id'])

    piece = instance

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
    solrconn.add(**d)
    solrconn.commit()


@receiver(post_delete, sender=DCPiece)
def solr_delete(sender, instance, **kwargs):
    from django.conf import settings
    import solr
    solrconn = solr.SolrConnection(settings.SOLR_SERVER)
    record = solrconn.query("type:duchemin_piece book_id:{0}".format(instance.id))
    if record:
        # the record already exists, so we'll remove it first.
        solrconn.delete(record.results[0]['id'])
