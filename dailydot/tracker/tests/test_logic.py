from http import HTTPStatus

from tracker.tests.fixture import BaseTestCase
from tracker.models import Habit


class HabitCreateTests(BaseTestCase):

    def test_authenticated_user_can_create_habit(self):
        Habit.objects.all().delete()

        response = self.author_client.post(
            self.habit_create_url, self.form_data
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        habit = Habit.objects.get()

        self.assertEqual(habit.user, self.author_user)
        self.assertEqual(habit.name, self.form_data["name"])

    def test_anonymous_user_cannot_create_note(self):
        Habit.objects.all().delete()

        response = self.client.post(self.habit_create_url, self.form_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Habit.objects.count(), 0)


class HabitEditDeleteTests(BaseTestCase):

    def test_user_can_delete_own_habit(self):
        initial_habit_count = Habit.objects.count()

        response = self.author_client.post(self.habit_delete_url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        final_note_count = Habit.objects.count()

        self.assertEqual(final_note_count, initial_habit_count - 1)

    def test_user_cannot_delete_others_notes(self):

        initial_habit_count = Habit.objects.count()

        response = self.reader_client.post(self.habit_delete_url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        final_note_count = Habit.objects.count()

        self.assertEqual(final_note_count, initial_habit_count)
