from django.test import TestCase
from django.core.urlresolvers import reverse


class RegistrationTest(TestCase):

    def test_show_registration_form(self):
        response = self.client.get(reverse('nonprofit:sign-up'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'atados/nonprofit/sign-up.html')

