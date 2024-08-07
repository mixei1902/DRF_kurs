from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from .models import Habit


class HabitTests(APITestCase):
    def setUp(self):
        """
        Создание пользователя и аутентификация клиента.
        """
        self.user = User.objects.create(
            email="user@example.com", password="password123"
        )
        self.client.login(email="user@example.com", password="password123")
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """
        Тестирование создания новой привычки.
        """
        url = reverse("habit-list-create")
        data = {
            "place": "Дом",
            "time": "12:00:00",
            "action": "Читать книгу",
            "is_pleasant": False,
            "periodicity": 1,
            "reward": "Шоколад",
            "time_to_complete": 120,
            "is_public": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().action, "Читать книгу")

    def test_create_habit_with_linked_habit(self):
        """
        Тестирование создания привычки с связанной приятной привычкой.
        """
        linked_habit = Habit.objects.create(
            user=self.user,
            place="Улица",
            time="18:00:00",
            action="Прогулка",
            is_pleasant=True,
            periodicity=1,
            time_to_complete=30,
            is_public=False,
        )
        url = reverse("habit-list-create")
        data = {
            "place": "Дом",
            "time": "12:00:00",
            "action": "Читать книгу",
            "is_pleasant": False,
            "linked_habit": linked_habit.id,
            "periodicity": 1,
            "time_to_complete": 120,
            "is_public": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
        self.assertEqual(
            Habit.objects.get(action="Читать книгу").linked_habit, linked_habit
        )

    def test_list_habits(self):
        """
        Тестирование получения списка привычек пользователя.
        """
        Habit.objects.create(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="Читать книгу",
            is_pleasant=False,
            periodicity=1,
            reward="Шоколад",
            time_to_complete=120,
            is_public=True,
        )
        url = reverse("habit-list-create")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["action"], "Читать книгу")

    def test_retrieve_habit(self):
        """
        Тестирование получения информации о конкретной привычке.
        """
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="Читать книгу",
            is_pleasant=False,
            periodicity=1,
            reward="Шоколад",
            time_to_complete=120,
            is_public=True,
        )
        url = reverse("habit-detail", kwargs={"pk": habit.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Читать книгу")

    def test_update_habit(self):
        """
        Тестирование обновления привычки.
        """
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="Читать книгу",
            is_pleasant=False,
            periodicity=1,
            reward="Шоколад",
            time_to_complete=120,
            is_public=True,
        )
        url = reverse("habit-detail", kwargs={"pk": habit.id})
        data = {
            "place": "Офис",
            "time": "14:00:00",
            "action": "Читать книгу",
            "is_pleasant": False,
            "periodicity": 1,
            "reward": "Шоколад",
            "time_to_complete": 120,
            "is_public": True,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.get().place, "Офис")

    def test_delete_habit(self):
        """
        Тестирование удаления привычки.
        """
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="Читать книгу",
            is_pleasant=False,
            periodicity=1,
            reward="Шоколад",
            time_to_complete=120,
            is_public=True,
        )
        url = reverse("habit-detail", kwargs={"pk": habit.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_list_public_habits(self):
        """
        Тестирование получения списка публичных привычек.
        """
        Habit.objects.create(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="Читать книгу",
            is_pleasant=False,
            periodicity=1,
            reward="Шоколад",
            time_to_complete=120,
            is_public=True,
        )
        url = reverse("public-habit-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["action"], "Читать книгу")
