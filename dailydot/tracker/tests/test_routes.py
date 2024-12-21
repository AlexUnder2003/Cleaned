from http import HTTPStatus

from tracker.tests.fixture import BaseTestCase


class PublicAccessTests(BaseTestCase):
    """Тесты для маршрутов, доступных всем пользователям."""

    def test_pages_accessible(self):
        urls = (
            self.home_page_url,
            self.login_url,
            self.signup_url,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)


class AnonymousAccessTests(BaseTestCase):
    """Тесты для анонимного пользователя."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.protected_urls = (
            cls.habit_create_url,
            cls.habit_detail_url,
            cls.habit_delete_url,
            cls.habit_reset_url,
            cls.profile_url,
        )

    def test_redirect_to_login(self):
        for url in self.protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, self.login_url + f"?next={url}")


class AuthenticatedAccessTests(BaseTestCase):
    """Тесты для аутентифицированного пользователя: автор и ридер."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.author_accessible_pages = (
            (cls.habit_detail_url, HTTPStatus.OK),
            (cls.habit_reset_url, HTTPStatus.FOUND),
            (cls.habit_delete_url, HTTPStatus.FOUND),
            (cls.profile_url, HTTPStatus.OK),
        )

        cls.reader_forbidden_pages = (
            (cls.habit_reset_url, HTTPStatus.NOT_FOUND),
            (cls.habit_delete_url, HTTPStatus.NOT_FOUND),
            (cls.profile_url, HTTPStatus.FORBIDDEN),
        )

    def test_author_pages_accessible(self):
        for url, expected_status in self.author_accessible_pages:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_reader_forbidden_pages(self):
        for url, expected_status in self.reader_forbidden_pages:
            with self.subTest(url=url):
                response = self.reader_client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirect_when_no_habits(self):
        response = self.reader_client.get(self.habit_detail_reader_url)
        self.assertRedirects(response, self.habit_create_url)
