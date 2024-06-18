from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import (RelatedHabitValidators, LeadTimeValidator, RelatedGoodHabitValidator,
                               GoodHabitNotAwardAndRelatedHabitValidator, RepeatValidator)


class HabitSerializer(ModelSerializer):
    """Сериализатор для модели Habit"""
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            RelatedHabitValidators(related_habit='related_habit', award='award'),
            LeadTimeValidator(lead_time='lead_time'),
            RelatedGoodHabitValidator(related_habit='related_habit', good_habit='good_habit'),
            GoodHabitNotAwardAndRelatedHabitValidator(good_habit='good_habit', award='award',
                                                      related_habit='related_habit'),
            RepeatValidator(period='period')
        ]
