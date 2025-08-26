from rest_framework import serializers
from .models import (
    User, LoginHistory, Address, Contact, Note, Category, Subject, File,
    Sharing, Notification, NotificationType, Review, NoteAnalysis,
    NoteSuggestion, ChatInteraction, NoteRecommendation, SearchLog,
    NoteTag, NoteEntity, UserInteraction, NoteHistory
)

# --------------------- Validações Customizadas ---------------------
def validate_postal_code(value):
    if not value.replace('-', '').isdigit() or len(value.replace('-', '')) != 8:
        raise serializers.ValidationError("CEP deve conter 8 dígitos no formato 00000-000.")
    return value

def validate_phone(value):
    cleaned = ''.join(filter(str.isdigit, value))
    if len(cleaned) < 10 or len(cleaned) > 15:
        raise serializers.ValidationError("Telefone deve ter entre 10 e 15 dígitos.")
    return value

# --------------------- Serializadores Principais ---------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'date_of_birth', 
            'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = ['id', 'user', 'timestamp', 'ip_address', 'user_agent']
        read_only_fields = ['id', 'timestamp']

class AddressSerializer(serializers.ModelSerializer):
    postal_code = serializers.CharField(validators=[validate_postal_code])

    class Meta:
        model = Address
        fields = [
            'id', 'user', 'state', 'street', 'number', 
            'complement', 'neighborhood', 'city', 'postal_code'
        ]
        read_only_fields = ['id']

class ContactSerializer(serializers.ModelSerializer):
    mobile_phone = serializers.CharField(validators=[validate_phone])
    landline = serializers.CharField(
        validators=[validate_phone], 
        required=False, 
        allow_blank=True
    )

    class Meta:
        model = Contact
        fields = ['id', 'user', 'landline', 'mobile_phone']
        read_only_fields = ['id']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'note', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

class NoteSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        source='categories',
        write_only=True
    )
    
    subjects = SubjectSerializer(many=True, read_only=True)
    subject_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Subject.objects.all(),
        source='subjects',
        write_only=True
    )
    
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = [
            'id', 'user', 'title', 'content', 'created_at', 'updated_at',
            'completed', 'categories', 'category_ids', 'subjects', 'subject_ids', 'files'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'files']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("O título não pode estar vazio.")
        return value

class SharingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sharing
        fields = ['id', 'note', 'shared_with', 'shared_at', 'can_edit']
        read_only_fields = ['id', 'shared_at']

class NotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationType
        fields = ['id', 'name', 'description', 'template']
        read_only_fields = ['id']

class NotificationSerializer(serializers.ModelSerializer):
    type = NotificationTypeSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'type', 'user', 'note', 'message', 
            'sent_at', 'read'
        ]
        read_only_fields = ['id', 'sent_at', 'message']

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'note', 'reviewer', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

# --------------------- Serializadores de IA ---------------------
class NoteAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteAnalysis
        fields = ['id', 'note', 'summary', 'sentiment', 'keywords', 'created_at']
        read_only_fields = ['id', 'created_at']

class NoteSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteSuggestion
        fields = ['id', 'note', 'suggestion', 'created_at', 'applied']
        read_only_fields = ['id', 'created_at']

class ChatInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatInteraction
        fields = ['id', 'user', 'message', 'response', 'timestamp', 'note_context']
        read_only_fields = ['id', 'timestamp']

class NoteRecommendationSerializer(serializers.ModelSerializer):
    recommended_note = serializers.StringRelatedField()

    class Meta:
        model = NoteRecommendation
        fields = [
            'id', 'user', 'recommended_note', 'score', 
            'algorithm_version', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

# --------------------- Serializadores de Logs ---------------------
class SearchLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchLog
        fields = ['id', 'user', 'query', 'results_count', 'created_at']
        read_only_fields = ['id', 'created_at']

class NoteTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteTag
        fields = ['id', 'note', 'tag']
        read_only_fields = ['id']

class NoteEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteEntity
        fields = ['id', 'note', 'entity_type', 'entity_value']
        read_only_fields = ['id']

class UserInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = ['id', 'user', 'note', 'interaction_type', 'timestamp', 'metadata']
        read_only_fields = ['id', 'timestamp']

class NoteHistorySerializer(serializers.ModelSerializer):
    edited_by = serializers.StringRelatedField()

    class Meta:
        model = NoteHistory
        fields = [
            'id', 'note', 'edited_by', 'previous_content', 
            'updated_content', 'change_reason', 'edited_at'
        ]
        read_only_fields = ['id', 'edited_at']