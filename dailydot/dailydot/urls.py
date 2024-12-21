from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView
from users.forms import CustomUserCreationForm
from users.views import custom_login

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls", namespace="main")),
    path("auth/login/", custom_login, name="customlogin"),
    path("auth/", include("django.contrib.auth.urls")),
    path(
        "auth/registration/",
        CreateView.as_view(
            template_name="registration/registration_form.html",
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy("main:index"),
        ),
        name="registration",
    ),
    path("habit/", include("tracker.urls", namespace="habits")),
    path("profile/", include("users.urls", namespace="users")),
]
