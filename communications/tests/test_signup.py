from django.test import TestCase
from django.urls import reverse


class SubscribeViewTests(TestCase):
    def test_planting_interest_page_is_a_static_splash_page(self):
        response = self.client.get(reverse("communications:planting-interest"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "communications/planting_interest.html")
        self.assertContains(response, "A team is taking shape")
        self.assertContains(response, 'href="mailto:contact@sojourn-church.com"', html=False)

    def test_signup_page_has_one_replaceable_zoho_signup_slot(self):
        response = self.client.get(reverse("communications:subscribe"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "communications/subscribe.html")
        self.assertContains(response, 'id="zcampaignOptinForm"')
        self.assertContains(response, 'id="sf3z66957effaa576e9ce498bb59685eb0373bbafcf97deaf9bda0f11fff8e457a3a"')
        self.assertContains(response, "optin.min.js")
        self.assertEqual(response.content.decode().count('id="zcampaignOptinForm"'), 1)
        self.assertEqual(response.content.decode().count('id="Zc_SignupSuccess"'), 1)
        self.assertEqual(response.content.decode().count('id="signupSuccessMsg"'), 1)

    def test_signup_page_renders_spanish_interface_text(self):
        response = self.client.get("/es/subscribe/")

        self.assertContains(response, '<html lang="es"', html=False)
        self.assertContains(response, 'name="robots" content="noindex,follow"', html=False)
        self.assertContains(response, "Mantente conectado")
        self.assertContains(response, "Iglesia Sojourn")

    def test_subscription_confirmation_page_uses_site_layout(self):
        response = self.client.get(reverse("communications:subscribe-confirmed"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "communications/subscribe_confirmed.html")
        self.assertContains(response, "Subscription confirmed")
        self.assertContains(response, 'class="site-header sticky-top"')

    def test_subscription_confirmation_page_renders_spanish_text(self):
        response = self.client.get("/es/subscribe/confirmed/")

        self.assertContains(response, "Suscripción confirmada")
