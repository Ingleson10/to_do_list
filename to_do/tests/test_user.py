import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'to_do_list.settings'
django.setup()

@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='password123'
    )

@pytest.fixture
def api_client():
    return APIClient()

# Testes para o endpoint de criação de usuário
def test_create_user(api_client):
    url = '/users/'
    data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123',
        'date_of_birth': '1990-01-01'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['username'] == 'newuser'

# Teste de leitura de um usuário
def test_get_user(api_client, user):
    url = f'/users/{user.id}/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == user.username

# Teste de atualização de um usuário
def test_update_user(api_client, user):
    url = f'/users/{user.id}/'
    data = {'username': 'updateduser', 'email': 'updateduser@example.com'}
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == 'updateduser'

# Teste de exclusão de um usuário
def test_delete_user(api_client, user):
    url = f'/users/{user.id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not get_user_model().objects.filter(id=user.id).exists()
