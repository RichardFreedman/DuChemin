from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


class DCBook(models.Model):
    class Meta:
        app_label = "duchemin"
        verbose_name = "Book"
        verbose_name_plural = "Books"

    book_id = models.IntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    complete_title = models.CharField(max_length=128, blank=True, null=True)
    publisher = models.CharField(max_length=64, blank=True, null=True)
    place_publication = models.CharField(max_length=64, blank=True, null=True)
    date = models.CharField(max_length=64, blank=True, null=True)
    volumes = models.CharField(max_length=64, blank=True, null=True)
    part_st_id = models.CharField(max_length=16, blank=True, null=True)
    part_cb_id = models.CharField(max_length=16, blank=True, null=True)
    num_compositions = models.CharField(max_length=16, blank=True, null=True)
    num_pages = models.CharField(max_length=16, blank=True, null=True)
    location = models.CharField(max_length=16, blank=True, null=True)
    rism = models.CharField(max_length=16, blank=True, null=True)
    cesr = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "{0}".format(self.title)


@receiver(post_save, sender=DCBook)
def solr_index(sender, instance, created, **kwargs):
    import uuid
    from django.conf import settings
    import solr

    solrconn = solr.SolrConnection(settings.SOLR_SERVER)
    record = solrconn.query("type:duchemin_book book_id:{0}".format(instance.id))
    if record:
        # the record already exists, so we'll remove it first.
        solrconn.delete(record.results[0]['id'])

    book = instance
    d = {
        'type': 'duchemin_book',
        'id': str(uuid.uuid4()),
        'book_id': int(book.book_id),
        'book_title': book.title,
    }
    solrconn.add(**d)
    solrconn.commit()


@receiver(post_delete, sender=DCBook)
def solr_delete(sender, instance, **kwargs):
    from django.conf import settings
    import solr
    solrconn = solr.SolrConnection(settings.SOLR_SERVER)
    record = solrconn.query("type:duchemin_book book_id:{0}".format(instance.id))
    if record:
        # the record already exists, so we'll remove it first.
        solrconn.delete(record.results[0]['id'])
