from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from tracker.models import Habit

User = get_user_model()


class BaseTestCase(TestCase):
    """Базовый класс для тестов."""

    @classmethod
    def setUpTestData(cls):
        cls.reader_user = User.objects.create_user(username="reader_user")
        cls.author_user = User.objects.create_user(username="author_user")

        cls.habit_by_author = Habit.objects.create(
            name="Author tests", user=cls.author_user
        )

        cls.form_data = {"name": "Habit by author"}
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader_user)

        cls.author_client = Client()
        cls.author_client.force_login(cls.author_user)

        cls.home_page_url = reverse("main:index")
        cls.habit_create_url = reverse("habits:create")
        cls.habit_detail_url = reverse(
            "habits:habit_detail",
            kwargs={"username": cls.author_user.username, "habit_id": 1},
        )

        cls.habit_detail_reader_url = reverse(
            "habits:habit_detail",
            kwargs={"username": cls.reader_user.username, "habit_id": 1},
        )
        cls.habit_delete_url = reverse("habits:delete", args=[1])
        cls.habit_reset_url = reverse("habits:reset", args=[1])

        cls.profile_url = reverse(
            "users:user_profile", args=[cls.author_user.username]
        )

        cls.login_url = reverse("customlogin")
        cls.logout_url = reverse("logout")
        cls.signup_url = reverse("registration")
