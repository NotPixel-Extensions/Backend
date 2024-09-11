from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Pictures
import json

class UserAPITestCase(APITestCase):

    def test_create_user(self):
        url = reverse('create-user')
        data = {"telegram_id": 123456789}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().telegram_id, 123456789)

    def test_update_last_request(self):
        user = User.objects.create(telegram_id=123456789)
        url = reverse('update-last-request', args=[user.telegram_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(User.objects.get(telegram_id=123456789).last_request)

    def test_create_picture(self):
        user = User.objects.create(telegram_id=123456789)
        url = reverse('create-picture', args=[user.id])
        data = {"data": {"key": "value"}}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pictures.objects.count(), 1)
        self.assertEqual(Pictures.objects.get().data, {"key": "value"})

    def test_list_user_pictures(self):
        user = User.objects.create(telegram_id=123456789)
        Pictures.objects.create(user=user, data={"key": "value"})
        Pictures.objects.create(user=user, data={"another_key": "another_value"})
        
        url = reverse('list-user-pictures', args=[user.telegram_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pictures = json.loads(response.content)["pictures"]
        self.assertEqual(len(pictures), 2)
        self.assertEqual(pictures[0]["data"], {"key": "value"})
        self.assertEqual(pictures[1]["data"], {"another_key": "another_value"})
