from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Habit(models.Model):
    name = models.CharField(max_length=255, help_text="Введите текст здесь")
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="habits"
    )

    habit_id = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.habit_id is None:
            last_habit = (
                Habit.objects.filter(user=self.user)
                .order_by("-habit_id")
                .first()
            )
            self.habit_id = last_habit.habit_id + 1 if last_habit else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (ID: {self.habit_id})"

    class Meta:
        ordering = ["creation_date"]
        unique_together = ("user", "habit_id")
