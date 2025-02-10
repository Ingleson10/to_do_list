from django.test import TestCase
from to_do.models import User, Note, Category

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")

class NoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@example.com")

    def test_create_note(self):
        note = Note.objects.create(user=self.user, title="Test Note", content="This is a test note.")
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.content, "This is a test note.")

class CategoryModelTest(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name="Work", description="Work-related tasks")
        self.assertEqual(category.name, "Work")
        self.assertEqual(category.description, "Work-related tasks")
