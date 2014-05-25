from rest_framework import generics
from rest_framework.renderers import JSONRenderer

from duchemin.serializers.phrase import DCPhraseSerializer
from duchemin.models.phrase import DCPhrase
from duchemin.renderers.custom_html_renderer import CustomHTMLRenderer


class PhraseListHTMLRenderer(CustomHTMLRenderer):
    template_name = "phrase/phrase_list.html"


class PhraseDetailHTMLRenderer(CustomHTMLRenderer):
    template_name = "phrase/phrase_detail.html"


class PhraseList(generics.ListAPIView):
    model = DCPhrase
    serializer_class = DCPhraseSerializer
    renderer_classes = (JSONRenderer, PhraseListHTMLRenderer)
    paginate_by = 100
    paginate_by_param = 'page_size'
    max_paginate_by = 200


class PhraseDetail(generics.RetrieveAPIView):
    model = DCPhrase
    serializer_class = DCPhraseSerializer
    renderer_classes = (JSONRenderer, PhraseDetailHTMLRenderer)
