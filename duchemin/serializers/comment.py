from django.contrib.auth.models import User
from duchemin.models.comment import DCComment
from duchemin.models.piece import DCPiece
from duchemin.models.userprofile import DCUserProfile
from duchemin.models.person import DCPerson
from rest_framework import serializers


class DCPersonCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DCPerson
        fields = ('person_id',)


class DCUserProfileCommentSerializer(serializers.HyperlinkedModelSerializer):
    person = DCPersonCommentSerializer()

    class Meta:
        model = DCUserProfile
        fields = ('person',)


class DCUserCommentSerializer(serializers.HyperlinkedModelSerializer):
    profile = DCUserProfileCommentSerializer()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'profile',)


class DCPieceCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DCPiece
        fields = ('piece_id',)


class DCCommentSerializer(serializers.HyperlinkedModelSerializer):
    author = DCUserCommentSerializer()
    piece = DCPieceCommentSerializer()

    class Meta:
        model = DCComment
        fields = ('id', 'author', 'piece', 'created', 'text',)
