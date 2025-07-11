import pytest
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from to_do.models import User, Address, Note, Category, NoteAnalysis, NoteSuggestions

@pytest.mark.django_db
class TestUserModel:
    def test_user_creation(self):
        # Testando criação de usuário com dados básicos
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        assert user.username == 'testuser'
        assert user.email == 'testuser@example.com'
        assert user.check_password('password123')

    def test_user_email_unique(self):
        # Testando que o campo email é único
        User.objects.create_user(
            username='user1',
            email='unique@example.com',
            password='password123'
        )
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                username='user2',
                email='unique@example.com',
                password='password123'
            )

    def test_user_email_required(self):
        # Testando que o email é obrigatório
        with pytest.raises(ValueError):
            User.objects.create_user(
                username='user2',
                password='password123'
            )

    def test_user_date_of_birth(self):
        # Testando a data de nascimento do usuário
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            date_of_birth='1990-01-01'
        )
        assert user.date_of_birth == '1990-01-01'

@pytest.mark.django_db
class TestAddressModel:
    def test_address_creation(self):
        # Testando a criação de um endereço
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        address = Address.objects.create(
            user=user,
            state='SP',
            street='Rua Teste',
            number='123',
            neighborhood='Bairro Teste',
            city='São Paulo',
            postal_code='12345-678'
        )
        assert address.user == user
        assert address.state == 'SP'
        assert address.city == 'São Paulo'

    def test_address_state_choices(self):
        # Testando que o campo state usa as opções corretas
        address = Address(state='XX', street='Rua Teste', number='123', neighborhood='Bairro Teste', city='São Paulo', postal_code='12345-678')
        with pytest.raises(ValidationError):
            address.full_clean()

@pytest.mark.django_db
class TestNoteModel:
    def test_note_creation(self):
        # Testando a criação de uma nota
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        note = Note.objects.create(
            user=user,
            title='Test Note',
            content='This is a test note.'
        )
        assert note.title == 'Test Note'
        assert note.content == 'This is a test note.'

    def test_note_unique_title_per_user(self):
        # Testando a restrição de título único por usuário
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        Note.objects.create(
            user=user,
            title='Unique Title',
            content='First note content.'
        )
        with pytest.raises(IntegrityError):
            Note.objects.create(
                user=user,
                title='Unique Title',
                content='Second note content.'
            )

@pytest.mark.django_db
class TestCategoryModel:
    def test_category_creation(self):
        # Testando a criação de uma categoria
        category = Category.objects.create(
            name='Test Category',
            description='This is a test category.'
        )
        assert category.name == 'Test Category'
        assert category.description == 'This is a test category.'

    def test_category_unique_name(self):
        # Testando que o nome da categoria é único
        Category.objects.create(
            name='Unique Category',
            description='This is a unique category.'
        )
        with pytest.raises(IntegrityError):
            Category.objects.create(
                name='Unique Category',
                description='Another unique category.'
            )

@pytest.mark.django_db
class TestNoteAnalysisModel:
    def test_note_analysis_creation(self):
        # Testando a criação de uma análise de nota
        note = Note.objects.create(
            user=User.objects.create_user(
                username='testuser',
                email='testuser@example.com',
                password='password123'
            ),
            title='Test Note',
            content='Content of the test note.'
        )
        analysis = NoteAnalysis.objects.create(
            note=note,
            summary='This is a summary of the note.',
            sentiment='positive'
        )
        assert analysis.note == note
        assert analysis.sentiment == 'positive'

    def test_note_analysis_sentiment_choices(self):
        # Testando a escolha do campo de sentimento
        note = Note.objects.create(
            user=User.objects.create_user(
                username='testuser',
                email='testuser@example.com',
                password='password123'
            ),
            title='Test Note',
            content='Content of the test note.'
        )
        analysis = NoteAnalysis(note=note, summary='summary', sentiment='invalid')
        with pytest.raises(ValidationError):
            analysis.full_clean()

@pytest.mark.django_db
class TestNoteSuggestionsModel:
    def test_note_suggestion_creation(self):
        # Testando a criação de sugestão de nota
        note = Note.objects.create(
            user=User.objects.create_user(
                username='testuser',
                email='testuser@example.com',
                password='password123'
            ),
            title='Test Note',
            content='Content of the test note.'
        )
        suggestion = NoteSuggestions.objects.create(
            note=note,
            suggestion='This is a suggestion for the note.'
        )
        assert suggestion.note == note
        assert suggestion.suggestion == 'This is a suggestion for the note.'
