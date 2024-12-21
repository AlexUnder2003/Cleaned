from django.urls import path

from tracker.views import (
    HabitCreateView,
    HabitDetailView,
    reset_creation_date,
    habit_delete,
)


app_name = "habits"

urlpatterns = [
    path(
        "<str:username>/<int:habit_id>/",
        HabitDetailView.as_view(),
        name="habit_detail",
    ),
    path("create/", HabitCreateView.as_view(), name="create"),
    path("reset/<int:habit_id>", reset_creation_date, name="reset"),
    path("delete/<int:habit_id>", habit_delete, name="delete"),
]
