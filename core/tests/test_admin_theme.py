from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class JazzminAdminTests(TestCase):
    def test_login_page_uses_sojourn_admin_welcome(self):
        response = self.client.get(reverse("admin:login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manage the Sojourn Church website")
        self.assertContains(response, "jazzmin/css/main.css")

    def test_dashboard_loads_for_staff_with_jazzmin_branding(self):
        user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="test-password",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sojourn Church")
        self.assertContains(response, "jazzmin/css/main.css")
