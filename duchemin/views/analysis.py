from rest_framework import generics
from rest_framework.renderers import JSONRenderer

from duchemin.serializers.analysis import DCAnalysisSerializer
from duchemin.models.analysis import DCAnalysis
from duchemin.renderers.custom_html_renderer import CustomHTMLRenderer


class AnalysisListHTMLRenderer(CustomHTMLRenderer):
    template_name = "analysis/analysis_list.html"


class AnalysisDetailHTMLRenderer(CustomHTMLRenderer):
    template_name = "analysis/analysis_detail.html"


class AnalysisList(generics.ListAPIView):
    model = DCAnalysis
    serializer_class = DCAnalysisSerializer
    renderer_classes = (JSONRenderer, AnalysisListHTMLRenderer)
    paginate_by = 100
    paginate_by_param = 'page_size'
    max_paginate_by = 200


class AnalysisDetail(generics.RetrieveAPIView):
    model = DCAnalysis
    serializer_class = DCAnalysisSerializer
    renderer_classes = (JSONRenderer, AnalysisDetailHTMLRenderer)
