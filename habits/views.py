from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitCreateAPIView(CreateAPIView):
    """Контроллер создания привычки."""
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitListAPIView(ListAPIView):
    """Контроллер для отображения списка всех привычек."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitRetrieveAPIView(RetrieveAPIView):
    """Контроллер для отображения конкретной привычки."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)


class HabitUpdateAPIView(UpdateAPIView):
    """Контроллер для обновления привычки."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)


class HabitDestroyAPIView(DestroyAPIView):
    """Контроллер для удаления привычки."""
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)


class PublicHabitListAPIView(ListAPIView):
    """Контроллер для отображения всех публичных привычек."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
