from django.urls import path

from users.views import UserProfileView

app_name = "users"

urlpatterns = [
    path(
        "<str:username>/",
        UserProfileView.as_view(),
        name="user_profile",
    ),
]
