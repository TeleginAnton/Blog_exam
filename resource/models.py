from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


def get_next_day():  # TODO У Вас увидел
    return timezone.now() + timedelta(days=1)


class Note(models.Model):
    class Status(models.IntegerChoices):
        POSTPONED = 0, _('Отложено')
        ACTIVE = 1, _('Активно')
        COMPLETED = 2, _('Выполнено')

    title = models.CharField(max_length=255, verbose_name=_('Заголовок'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Автор'))
    date_public = models.DateField(auto_now_add=True, verbose_name=_('Опубликовано'))
    status = models.IntegerField(default=Status.POSTPONED, verbose_name=_('Статус'))
    sign = models.BooleanField(default=False, verbose_name=_('Важно'))
    as_public = models.BooleanField(default=False, verbose_name=_('Публичная'))
    message = models.TextField(default=" ", verbose_name=_('Текст статьи'))
    public = models.BooleanField(default=False, verbose_name=_('Опубликовать'))
    update = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))
    date_of_completion = models.DateTimeField(default=get_next_day, verbose_name='Дата выполнения')

    def __str__(self):
        return f'Запись №{self.id}'

    class Meta:
        verbose_name = _('Запись')
        verbose_name_plural = _('Записи')


class Comment(models.Model):
    """ Комментарии и оценки к статьям """

    class Ratings(models.IntegerChoices):
        WITHOUT_RATING = 0, _('Без оценки')
        TERRIBLE = 1, _('Ужасно')
        BADLY = 2, _('Плохо')
        FINE = 3, _('Нормально')
        GOOD = 4, _('Хорошо')
        EXCELLENT = 5, _('Отлично')

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    rating = models.IntegerField(default=Ratings.WITHOUT_RATING, choices=Ratings.choices, verbose_name='Оценка')

    def __str__(self):
        return f'{self.get_rating_display()}: {self.author}'
