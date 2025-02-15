import pytest
from rest_framework import status
from rest_framework.test import APIClient
from models import Notification, User
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'to_do_list.settings'
django.setup()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='password123'
    )

@pytest.fixture
def notification(user):
    return Notification.objects.create(
        user=user,
        type="info",
        sent_at="2025-02-15T12:00:00Z",
        note=None
    )

@pytest.fixture
def api_client():
    return APIClient()

# Teste de leitura de notificações
def test_get_notifications(api_client, notification, user):
    api_client.force_authenticate(user=user)
    url = f'/notifications/{notification.id}/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['type'] == 'info'

# Teste de listagem de notificações
def test_list_notifications(api_client, user, notification):
    api_client.force_authenticate(user=user)
    url = '/notifications/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0

# Teste de leitura de notificações não lidas
def test_get_unread_notifications(api_client, user, notification):
    api_client.force_authenticate(user=user)
    url = '/notifications/unread/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1  # Assume que o teste cria uma notificação não lida
