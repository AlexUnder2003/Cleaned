from http import HTTPStatus

from tracker.forms import HabitForm
from tracker.tests.fixture import BaseTestCase


class DetailHabitViewTests(BaseTestCase):
    """Тесты для страницы привычки"""

    def test_habit_detail_context(self):
        response = self.author_client.get(self.habit_detail_url)

        self.assertEqual(response.status_code, 200)

        context = response.context

        habit_in_context = context["habit"]
        self.assertEqual(habit_in_context, self.habit_by_author)

        other_habits_in_context = context["other_habits"]
        self.assertTrue(
            all(
                habit.user == self.habit_by_author.user
                for habit in other_habits_in_context
            )
        )
        self.assertIn(self.habit_by_author, other_habits_in_context)

        self.assertEqual(
            context["current_habit_id"], self.habit_by_author.habit_id
        )

    def test_form_in_context(self):
        response = self.author_client.get(self.habit_create_url)

        self.assertEqual(response.status_code, 200)

        self.assertIn("form", response.context)

        self.assertIsInstance(response.context["form"], HabitForm)
