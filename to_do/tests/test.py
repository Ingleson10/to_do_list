from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from models import (
    LoginHistory, Note, NoteHistory
)

User = get_user_model()

class BaseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

# Removido UserViewSetTests

class LoginHistoryViewSetTests(BaseTestCase):
    def test_list_login_history(self):
        LoginHistory.objects.create(user=self.user, ip_address='127.0.0.1', user_agent='test')
        response = self.client.get(reverse('login-histories-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

# ... Mantenha todos os outros testes restantes sem alterações ...

class AddressViewSetTests(BaseTestCase):
    def test_create_address(self):
        data = {
            'state': 'SP',
            'street': 'Rua Teste',
            'number': '123',
            'neighborhood': 'Centro',
            'city': 'São Paulo',
            'postal_code': '01000100'
        }
        response = self.client.post(reverse('addresses-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user.address.postal_code, '01000100')

# ... Continue com os demais testes ...

class NoteHistoryViewSetTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.note = Note.objects.create(user=self.user, title='Test Note', content='Test Content')
        self.history = NoteHistory.objects.create(
            note=self.note,
            edited_by=self.user,
            previous_content='Old content',
            updated_content='New content',
            change_reason='Test update'
        )

    def test_list_note_history(self):
        response = self.client.get(reverse('note-history-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)