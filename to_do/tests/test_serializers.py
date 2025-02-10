from django.test import TestCase
from to_do.models import User, Note, Category
from to_do.serializers import UserSerializer, NoteSerializer, CategorySerializer

class UserSerializerTest(TestCase):
    def test_user_serializer(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data["username"], "testuser")
        self.assertEqual(serializer.data["email"], "testuser@example.com")

class NoteSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user=self.user) # Autentica o usuário
    def test_note_serializer(self):
        user = User.objects.create(username="testuser", email="testuser@example.com")
        note = Note.objects.create(user=user, title="Test Note", content="This is a test note.")
        serializer = NoteSerializer(note)
        self.assertEqual(serializer.data["title"], "Test Note")
        self.assertEqual(serializer.data["content"], "This is a test note.")
    class Meta:
        model = Note
        fields = ['id', 'title', 'description', 'completed']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class CategorySerializerTest(TestCase):
    def test_category_serializer(self):
        category = Category.objects.create(name="Work", description="Work-related tasks")
        serializer = CategorySerializer(category)
        self.assertEqual(serializer.data["name"], "Work")
        self.assertEqual(serializer.data["description"], "Work-related tasks")
