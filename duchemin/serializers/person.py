from duchemin.models.person import DCPerson
from duchemin.models.analysis import DCAnalysis
from duchemin.models.piece import DCPiece
from duchemin.models.phrase import DCPhrase
from duchemin.models.userprofile import DCUserProfile
from rest_framework import serializers


class DCPieceAnalysisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DCPiece
        fields = '__all__'

class DCPhraseAnalysisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DCPhrase
        fields = '__all__'

class DCPersonAnalysesSerializer(serializers.HyperlinkedModelSerializer):
    composition_number = DCPieceAnalysisSerializer()
    phrase_number = DCPhraseAnalysisSerializer()
    class Meta:
        model = DCAnalysis
        fields = '__all__'


class DCPersonListSerializer(serializers.HyperlinkedModelSerializer):
    full_name = serializers.CharField()
    class Meta:
        model = DCPerson
        fields = '__all__'


class DCPersonDetailSerializer(serializers.HyperlinkedModelSerializer):
    full_name = serializers.CharField()
    analyses = DCPersonAnalysesSerializer(many=True)
    class Meta:
        model = DCPerson
        fields = '__all__'