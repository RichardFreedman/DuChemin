from duchemin.models.phrase import DCPhrase
from duchemin.models.piece import DCPiece
from rest_framework import serializers


class DCPiecePhraseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DCPiece
        fields = ('piece_id',)


class DCPhraseSerializer(serializers.HyperlinkedModelSerializer):
    piece_id = DCPiecePhraseSerializer()

    class Meta:
        model = DCPhrase
        ('url', 'piece_id', 'phrase_num', 'text',
         'phrase_start', 'phrase_stop',
         'phrase_text', 'rhyme',)
