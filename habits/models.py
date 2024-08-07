from users.models import User
from django.db import models


class Habit(models.Model):
    """
    Модель для представления привычки.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, создатель привычки",
    )

    # Поле для места выполнения привычки
    place = models.CharField(
        max_length=100,
        verbose_name="Место",
        help_text="Место, в котором необходимо выполнять привычку",
    )

    # Поле для времени выполнения привычки
    time = models.TimeField(
        verbose_name="Время", help_text="Время, когда необходимо выполнять привычку"
    )

    # Поле для действия, которое представляет собой привычка
    action = models.CharField(
        max_length=255,
        verbose_name="Действие",
        help_text="Действие, которое представляет собой привычка",
    )

    # Поле для признака приятной привычки
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Признак того, что привычка является приятной",
    )

    # Поле для связанной привычки
    linked_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        help_text="Привычка, которая связана с другой привычкой",
    )

    # Поле для периодичности выполнения привычки
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность",
        help_text="Периодичность выполнения привычки для напоминания в днях",
    )

    # Поле для вознаграждения за выполнение привычки
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text="Чем пользователь должен себя вознаградить после выполнения",
    )

    # Поле для времени на выполнение привычки
    time_to_complete = models.PositiveIntegerField(
        default=120,
        verbose_name="Время на выполнение",
        help_text="Время, которое предположительно потратит пользователь на выполнение привычки в секундах",
    )

    # Поле для признака публичности привычки
    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
        help_text="Привычки можно публиковать в общий доступ, чтобы другие пользователи могли брать в пример чужие привычки",
    )

    def save(self, *args, **kwargs):
        # Проверка, чтобы не было заполнено одновременно поле вознаграждения и поле связанной привычки
        if self.linked_habit and self.reward:
            raise ValueError(
                "Нельзя одновременно указать и вознаграждение, и связанную привычку."
            )

        # Проверка, чтобы время на выполнение не превышало 120 секунд
        if self.time_to_complete > 120:
            raise ValueError("Время на выполнение не может превышать 120 секунд.")

        # Проверка, чтобы в связанные привычки попадали только привычки с признаком приятной привычки
        if self.linked_habit and not self.linked_habit.is_pleasant:
            raise ValueError("Связанная привычка должна быть приятной.")

        # Проверка, чтобы у приятной привычки не было вознаграждения или связанной привычки
        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValueError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        # Проверка, чтобы привычка выполнялась не реже, чем 1 раз в 7 дней
        if self.periodicity < 1 or self.periodicity > 7:
            raise ValueError("Периодичность должна быть в пределах от 1 до 7 дней.")

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["time"]

    def __str__(self):
        return f"Я буду{self.action} в {self.time} в {self.place}"
