from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from tracker.models import Habit
from tracker.forms import HabitForm

User = get_user_model()


class HabitDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Habit
    template_name = "tracker/detail.html"
    context_object_name = "habit"

    def get_object(self):
        username = self.kwargs["username"]
        habit_id = self.kwargs["habit_id"]
        user = get_object_or_404(User, username=username)
        habit = get_object_or_404(Habit, user=user, habit_id=habit_id)
        return habit

    def dispatch(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        user = get_object_or_404(User, username=username)

        if Habit.objects.filter(user=user).count() == 0:
            return redirect(reverse("habits:create"))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now()
        habit = context["habit"]
        days_since_creation = (today - habit.creation_date).days
        context["today"] = today
        context["days"] = days_since_creation
        context["current_habit_id"] = self.object.habit_id
        user_habits = Habit.objects.filter(user=habit.user)
        context["other_habits"] = user_habits
        return context

    def test_func(self):
        return self.request.user == self.get_object().user


class HabitCreateView(LoginRequiredMixin, CreateView):
    model = Habit
    form_class = HabitForm
    template_name = "tracker/create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "habits:habit_detail",
            kwargs={
                "habit_id": self.object.habit_id,
                "username": self.request.user.username,
            },
        )


@login_required
def reset_creation_date(request, habit_id):
    habit = get_object_or_404(Habit, user=request.user, habit_id=habit_id)

    habit.creation_date = timezone.now()
    habit.save()

    return HttpResponseRedirect(
        reverse(
            "habits:habit_detail",
            kwargs={"username": request.user.username, "habit_id": habit_id},
        )
    )


@login_required
def habit_delete(request, habit_id):
    habit = get_object_or_404(Habit, user=request.user, habit_id=habit_id)

    if habit.user != request.user:
        redirect(reverse("customlogin"))

    habit.delete()

    return redirect(
        reverse(
            "habits:habit_detail",
            kwargs={"username": request.user.username, "habit_id": 1},
        )
    )
