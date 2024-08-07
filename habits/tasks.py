from celery import shared_task
from django.utils import timezone
from .models import Habit
from .services import send_telegram_message


@shared_task
def send_habit_reminder():
    now = timezone.now()
    habits = Habit.objects.filter(
        time__lte=now.time(), periodicity=1
    )  # пример фильтрации
    for habit in habits:
        message = f"Напоминание: {habit.action} в {habit.time} в {habit.place}"
        send_telegram_message(habit.user.chat_id, message)
