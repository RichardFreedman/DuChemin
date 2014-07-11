import urlparse
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from django.shortcuts import get_object_or_404

from duchemin.models.note import DCNote
from duchemin.models.piece import DCPiece
from duchemin.serializers.note import DCNoteSerializer


class NoteList(generics.ListCreateAPIView):
    model = DCNote
    serializer_class = DCNoteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    paginate_by = 100
    paginate_by_param = 'page_size'
    max_paginate_by = 200

    def get_queryset(self):
        current_user = User.objects.get(pk=self.request.user.id)

        # Must filter by author to prevent making everyone's notes public
        queryset = DCNote.objects.filter(author=current_user)

        return queryset

    def post(self, request, *args, **kwargs):
        piece_id = request.DATA.get('piece_id', None)
        note_text = request.DATA.get('text', None)

        piece_obj = get_object_or_404(DCPiece, piece_id=piece_id)

        current_user = User.objects.get(pk=request.user.id)
        note = DCNote()
        note.piece = piece_obj
        note.author = current_user
        note.text = note_text

        # Since `current_user` was gotten from the login, we're not
        # letting just anybody write anywhere.
        note.save()

        serialized = DCNoteSerializer(note).data

        return Response(serialized, status=status.HTTP_201_CREATED)


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    model = DCNote
    serializer_class = DCNoteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    paginate_by = 100
    paginate_by_param = 'page_size'
    max_paginate_by = 200

    def get_queryset(self):
        current_user = User.objects.get(pk=self.request.user.id)

        # Must filter by author to prevent making everyone's notes public
        queryset = DCNote.objects.filter(author=current_user)

        return queryset
