from rest_framework.response import Response
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView

from resource.models import Note, Comment
from . import serializers, filters, settings_local


class NoteListApiView(ListCreateAPIView):
    """ Просмотр списка заметок"""
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = filters.NoteFilter

    ordering = ["status", "as_public"]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.order_by_queryset(queryset)

        return queryset

    def order_by_queryset(self, queryset):
        return queryset.order_by(*self.ordering)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PublicNoteListAPIView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.NoteFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset \
            .filter(public=True) \
            .order_by("date_public") \
            .prefetch_related("author", "comment_set")


class DetailAPIView(APIView):
    """Класс добавления, корректировки, удаления заметки"""
    @staticmethod
    def get_note(note_id, author_id):
        try:
            return Note.objects.get(id=note_id, author_id=author_id)

        except Note.DoesNotExist:
            return None

    @staticmethod
    def get(request, pk, *args, **kwargs):
        try:
            note_instance = Note.objects.get(id=pk)
        except Note.DoesNotExist:
            return None

        if not note_instance:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.NoteSerializer(note_instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):

        note_instance = self.get_note(pk, request.user.id)

        if not note_instance:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data = {'title': request.data.get('title'),
                'message': request.data.get('message'),
                'status': request.data.get('status'),
                'sign': request.data.get('sign'),
                'public': request.data.get('public'),
                'author': request.user.id}

        serializer = serializers.NoteSerializer(instance=note_instance, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):

        note_ = self.get_note(pk, request.user.id)

        if not note_:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        Note.objects.filter(id=pk).delete()
        return Response(status=status.HTTP_200_OK)


class CommentListCreateAPIView(ListCreateAPIView):
    """ Комментарии к публикациям"""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return serializer


class AboutTempLate(TemplateView):
    """Класс визуализации пользователя + версии сервера"""
    template_name = 'resource_api/About.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['server'] = settings_local.version_server()
        return context
