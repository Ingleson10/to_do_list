from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from to_do.models import User, Note, Category

class UserViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin", email="admin@example.com")
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        data = {"username": "testuser", "email": "testuser@example.com", "password": "password123"}
        response = self.client.post(reverse("user-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_users(self):
        User.objects.create(username="user1", email="user1@example.com")
        User.objects.create(username="user2", email="user2@example.com")
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class NoteViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@example.com")
        self.client.force_authenticate(user=self.user)

    def test_create_note(self):
        data = {"title": "Test Note", "content": "This is a test note.", "user": self.user.id}
        response = self.client.post(reverse("note-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_list_notes(self):
        Note.objects.create(user=self.user, title="Note 1", content="Content 1")
        Note.objects.create(user=self.user, title="Note 2", content="Content 2")
        response = self.client.get(reverse("note-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class CategoryViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@example.com")
        self.client.force_authenticate(user=self.user)

    def test_create_category(self):
        data = {"name": "Work", "description": "Work-related tasks"}
        response = self.client.post(reverse("category-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_categories(self):
        Category.objects.create(name="Personal", description="Personal tasks")
        response = self.client.get(reverse("category-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

