from django.test import TestCase
from django.core.urlresolvers import reverse


class RegistrationTest(TestCase):

    def test_show_sign_up_form(self):
        response = self.client.get(reverse('nonprofit:sign-up'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'atados_nonprofit/sign-up.html')

    def test_registration_post(self):
        response = self.client.post(reverse('nonprofit:sign-up'), {
            'nonprofit_name': 'Atados Test', 'slug': 'atados-test',
            'first_name': 'Guedes', 'email': 'guedes-test@atados.com.br',
            'username': 'guedes-test', 'password1': 'asdfgh',
            'password2': 'asdfgh'})
        self.assertEqual(302, response.status_code)
        self.assertEqual(response.get('Location'),
                         'http://testserver' + reverse('nonprofit:sign-up-complete'))
        self.assertTemplateUsed(response, 'atados_nonprofit/activation_email.txt')

    def test_sign_up_complete(self):
        response = self.client.get(reverse('nonprofit:sign-up-complete'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'atados_nonprofit/sign-up-complete.html')
