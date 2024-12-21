from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from users.forms import LoginForm


User = get_user_model()


def custom_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:

                login(request, user)

                return redirect(
                    "habits:habit_detail",
                    username=username,
                    habit_id=1,
                )
            else:

                form.add_error(None, "Неверное имя пользователя или пароль.")
    else:
        form = LoginForm()

    return render(request, "registration/login.html", {"form": form})


class UserProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    template_name = "users/profile.html"

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs["username"])

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context["habits"] = user.habits.all()
        return context
