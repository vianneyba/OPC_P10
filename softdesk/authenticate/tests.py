from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class TestSignup(APITestCase):
    url = reverse_lazy('signup')

    def test_create(self):
        self.assertFalse(User.objects.exists())
        data = {
            'first_name': 'maxime',
            'last_name': 'forestier',
            'email': 'maxime.forestier@free.fr',
            'password': 'lille59000'
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.exists())

        user = User.objects.get(email='maxime.forestier@free.fr')
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.email, data['email'])
