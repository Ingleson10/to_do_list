import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from models import Note
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
def note(user):
    return Note.objects.create(
        user=user,
        title="Test Note",
        content="This is a test note.",
        completed=False
    )

@pytest.fixture
def api_client():
    return APIClient()

# Teste de criação de uma nota
def test_create_note(api_client, user):
    api_client.force_authenticate(user=user)
    url = '/notes/'
    data = {
        'title': 'New Note',
        'content': 'Content of the new note',
        'completed': False
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'New Note'

# Teste de leitura de uma nota
def test_get_note(api_client, note, user):
    api_client.force_authenticate(user=user)
    url = f'/notes/{note.id}/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == note.title

# Teste de atualização de uma nota
def test_update_note(api_client, note, user):
    api_client.force_authenticate(user=user)
    url = f'/notes/{note.id}/'
    data = {'title': 'Updated Note', 'content': 'Updated content of the note'}
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'Updated Note'

# Teste de exclusão de uma nota
def test_delete_note(api_client, note, user):
    api_client.force_authenticate(user=user)
    url = f'/notes/{note.id}/'
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Note.objects.filter(id=note.id).exists()
