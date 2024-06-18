from rest_framework.serializers import ValidationError


class RelatedHabitValidators:
    """Исключить одновременный выбор связанной привычки и указания вознаграждения."""
    def __init__(self, related_habit, award):
        self.related_habit = related_habit
        self.award = award

    def __call__(self, value):
        related_habit = dict(value).get(self.related_habit)
        award = dict(value).get(self.award)
        if related_habit and award:
            raise ValidationError("Нельзя одновременно выбрать связанную привычку и вознаграждение.")


class LeadTimeValidator:
    """Время выполнения должно быть не больше 120 секунд."""
    def __init__(self, lead_time):
        self.lead_time = lead_time

    def __call__(self, value):
        lead_time = dict(value).get(self.lead_time)
        if int(lead_time) < 120:
            raise ValidationError("Время выполнения должно быть не больше 120 секунд.")


class RelatedGoodHabitValidator:
    """В связанные привычки могут попадать только привычки с признаком приятной привычки."""
    def __init__(self, related_habit, good_habit):
        self.related_habit = related_habit
        self.good_habit = good_habit

    def __call__(self, value):
        related_habit = dict(value).get(self.related_habit)
        if related_habit and not getattr(related_habit, 'good_habit', False):
            raise ValidationError("В связанные привычки могут попадать только привычки с признаком приятной привычки")


class GoodHabitNotAwardAndRelatedHabitValidator:
    """У приятной привычки не может быть вознаграждения или связанной привычки."""
    def __init__(self, good_habit, award, related_habit):
        self.good_habit = good_habit
        self.award = award
        self.related_habit = related_habit

    def __call__(self, value):
        good_habit = dict(value).get(self.good_habit)
        award = dict(value).get(self.award)
        related_habit = dict(value).get(self.related_habit)
        if good_habit and (award or related_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")


class RepeatValidator:
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней."""
    def __init__(self, period):
        self.period = period

    def __call__(self, value):
        period = dict(value).get(self.period)
        if period not in ['daily', 'three_days', 'weekly']:
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")
