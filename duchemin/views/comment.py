import urlparse
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from django.shortcuts import get_object_or_404

from duchemin.models.comment import DCComment
from duchemin.models.piece import DCPiece
from duchemin.serializers.comment import DCCommentSerializer

# These will stick around, but if we're only using this for JSON serialization
# we won't need HTML templates.
# from duchemin.renderers.custom_html_renderer import CustomHTMLRenderer
# class CommentListHTMLRenderer(CustomHTMLRenderer):
#     template_name = "comment/comment_list.html"


# class CommentDetailHTMLRenderer(CustomHTMLRenderer):
#     template_name = "comment/comment_detail.html"

class CommentList(generics.ListCreateAPIView):
    model = DCComment
    serializer_class = DCCommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,)
    paginate_by = 100
    paginate_by_param = 'page_size'
    max_paginate_by = 200

    def get_queryset(self):
        piece_id = self.request.QUERY_PARAMS.get('piece_id')
        last_update = self.request.QUERY_PARAMS.get('last_update')

        queryset = DCComment.objects.filter(id__gt=last_update)

        if piece_id:
            queryset = queryset.filter(piece=piece_id)

        return queryset

    def get(self, request, *args, **kwargs):
        last_update = request.QUERY_PARAMS.get("last_update", None)
        if not last_update:
            return Response({'message': 'You must provide the last_update query parameter'}, status=status.HTTP_400_BAD_REQUEST)

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        piece_url = request.DATA.get('piece', None)
        value = urlparse.urlparse(piece_url).path

        try:
            p = resolve(value)
        except:
            return Response({"message": "Could not resolve {0} to a Piece"}, status=status.HTTP_400_BAD_REQUEST)

        piece_obj = get_object_or_404(DCPiece, pk=p.kwargs.get("pk"))

        current_user = User.objects.get(pk=request.user.id)
        comment = DCComment()
        comment.piece = piece_obj
        comment.author = current_user
        comment.text = request.DATA.get('text', None)
        comment.save()

        serialized = DCCommentSerializer(comment).data

        return Response(serialized, status=status.HTTP_201_CREATED)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    model = DCComment
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = DCCommentSerializer
    renderer_classes = (JSONRenderer,)
