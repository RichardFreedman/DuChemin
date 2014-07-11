from django.contrib.auth.models import User
from duchemin.models.note import DCNote
from duchemin.models.piece import DCPiece
from rest_framework import serializers


class DCUserNoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class DCPieceNoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DCPiece
        fields = ('piece_id',)


class DCNoteSerializer(serializers.HyperlinkedModelSerializer):
    author = DCUserNoteSerializer()
    piece = DCPieceNoteSerializer()

    class Meta:
        read_only = False
        model = DCNote
        fields = ('url', 'author', 'piece', 'updated', 'text',)
