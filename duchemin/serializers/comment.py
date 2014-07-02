from django.contrib.auth.models import User
from duchemin.models.comment import DCComment
from duchemin.models.piece import DCPiece
from rest_framework import serializers

# class DCPieceAnalysisSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = DCPiece


# class DCPhraseAnalysisSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = DCPhrase

class DCUserCommentSerializer(serializers.RelatedField):
    class Meta:
        read_only = False
        model = User
        fields = ('url', 'username', 'first_name', 'last_name')

class DCPieceCommentSerializer(serializers.RelatedField):
    class Meta:
        read_only = False
        model = DCPiece
        fields = ('piece_id')

class DCCommentSerializer(serializers.HyperlinkedModelSerializer):
    author = DCUserCommentSerializer()
    piece = DCPieceCommentSerializer()

    class Meta:
        model = DCComment
