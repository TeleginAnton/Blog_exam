from django_filters import rest_framework as filters

from resource.models import Note


class NoteFilter(filters.FilterSet):
    status = filters.NumberFilter(
        field_name="update",
        lookup_expr='year',
        help_text='Год статьи',
    )

    class Meta:
        model = Note
        fields = [
            'status',
            'sign',
            'as_public',
        ]

