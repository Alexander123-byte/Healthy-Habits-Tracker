from django.conf import settings
from django.db import models


class Habit(models.Model):
    """Модель описания привычки"""

    ACTION_CHOICES = [
        ('walk', 'гулять'),
        ('study', 'учиться'),
        ('work', 'работать'),
        ('clean', 'прибраться'),
        ('eat', 'покушать'),
    ]

    PERIOD_CHOICES = [
        ('daily', 'ежедневно'),
        ('three_days', 'каждые 3 дня'),
        ('weekly', 'еженедельно'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Пользователь')
    place = models.CharField(max_length=100, verbose_name='Место')
    time = models.DateTimeField(verbose_name='Время выполнения привычки')
    action = models.CharField(max_length=100, choices=ACTION_CHOICES, verbose_name='Действие')
    good_habit = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                      verbose_name='Связанная привычка')
    period = models.CharField(max_length=30, choices=PERIOD_CHOICES, default='weekly',
                              verbose_name='Периодичность')
    award = models.CharField(max_length=150, null=True, blank=True, verbose_name='Вознаграждение')
    lead_time = models.IntegerField(verbose_name='Время на выполнение (секунды)')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return f'Я буду {self.action} в {self.time} в {self.place}'
