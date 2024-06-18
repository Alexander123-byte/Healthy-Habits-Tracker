from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.utils import timezone
import datetime

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru", password="12345")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            place="на улице",
            time=timezone.make_aware(datetime.datetime(2024, 5, 30)),
            action="walk",
            good_habit=True,
            period="daily",
            lead_time=60,
            is_public=False,
            user=self.user
        )

    def test_create_habit(self):
        url = reverse("habits:habit_create")
        data = {
            "user": self.user.pk,
            "place": "дома",
            "time": "2024-05-30",
            "action": "clean",
            "good_habit": True,
            "period": "weekly",
            "lead_time": 100,
            "is_public": True,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)
        self.assertTrue(Habit.objects.all().exists())

    def test_habit_retrieve(self):
        url = reverse("habits:habit_detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_update(self):
        url = reverse("habits:habit_update", args=(self.habit.pk,))
        data = {
            "place": "обновить место",
            "action": "walk",
            "period": "daily",
            "lead_time": 60,
            "good_habit": self.habit.good_habit,
            "time": self.habit.time.isoformat()
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.get(pk=self.habit.pk).place, "обновить место")

    def test_habit_delete(self):
        url = reverse("habits:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_habit_list(self):
        url = reverse("habits:habit_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "place": "на улице",
                    "time": "2024-05-30T00:00:00Z",
                    "action": self.habit.action,
                    "good_habit": self.habit.good_habit,
                    "period": self.habit.period,
                    "award": None,
                    "lead_time": 60,
                    "is_public": self.habit.is_public,
                    "user": self.user.pk,
                    "related_habit": None
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_habit_public(self):
        url = reverse("habits:public_habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
