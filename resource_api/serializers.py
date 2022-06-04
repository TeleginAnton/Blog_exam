from rest_framework import serializers

from resource.models import Note, Comment


class NoteSerializer(serializers.ModelSerializer):
    """Класс для сериализации заметок"""
    class Meta:
        model = Note
        fields = '__all__'
        red_only_fields = ('Author',)


class CommentSerializer(serializers.ModelSerializer):
    """Класс для сериализации комментариев"""
    class Meta:
        model = Comment
        fields = '__all__'
        red_only_fields = ('Author',)
