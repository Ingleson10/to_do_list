from rest_framework import serializers
from .models import (
    User, LoginHistory, Address, Contact, Note, Category, Subject, File, 
    Sharing, Notification, NotificationType, Review, NoteAnalysis, 
    NoteSuggestions, ChatInteraction, NoteRecommendation, SearchLog, 
    NoteTags, NoteEntities, UserInteraction, NoteHistory
)

# Funções auxiliares para validação
def validate_postal_code(value):
    if len(value) != 8:
        raise serializers.ValidationError("Postal code must have 8 characters.")
    return value

def validate_phone(value):
    if len(value) < 10 or len(value) > 15:
        raise serializers.ValidationError("Phone number should have between 10 and 15 digits.")
    return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = ['id', 'user', 'timestamp', 'ip_address', 'user_agent']
        read_only_fields = ['id', 'timestamp']

    def validate_ip_address(self, value):
        # Adicionar validação customizada para IP, se necessário
        return value

class AddressSerializer(serializers.ModelSerializer):
    postal_code = serializers.CharField(validators=[validate_postal_code])  # Validação de código postal

    class Meta:
        model = Address
        fields = ['id', 'user', 'state', 'street', 'number', 'complement', 'neighborhood', 'city', 'postal_code']
        read_only_fields = ['id']

class ContactSerializer(serializers.ModelSerializer):
    mobile_phone = serializers.CharField(validators=[validate_phone])  # Validação do telefone

    class Meta:
        model = Contact
        fields = ['id', 'user', 'landline', 'mobile_phone']
        read_only_fields = ['id']

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at', 'completed', 'categories', 'subjects']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'note', 'file']
        read_only_fields = ['id']

class SharingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sharing
        fields = ['id', 'note', 'shared_with']
        read_only_fields = ['id']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'type', 'sent_at', 'note', 'user']
        read_only_fields = ['id', 'sent_at']

class NotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationType
        fields = ['id', 'name']
        read_only_fields = ['id']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'note', 'rating', 'comment']
        read_only_fields = ['id']

# Serializers para IA e funcionalidades de recomendação

class NoteAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteAnalysis
        fields = ['id', 'note', 'summary', 'sentiment', 'created_at']
        read_only_fields = ['id', 'created_at']

class NoteSuggestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteSuggestions
        fields = ['id', 'note', 'suggestion', 'created_at']
        read_only_fields = ['id', 'created_at']

class ChatInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatInteraction
        fields = ['id', 'user', 'message', 'response', 'timestamp']
        read_only_fields = ['id', 'timestamp']

class NoteRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteRecommendation
        fields = ['id', 'user', 'recommended_note', 'score', 'created_at']
        read_only_fields = ['id', 'created_at']

class SearchLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchLog
        fields = ['id', 'user', 'query', 'search_results', 'created_at']
        read_only_fields = ['id', 'created_at']

class NoteTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteTags
        fields = ['id', 'note', 'tag_name']
        read_only_fields = ['id']

class NoteEntitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteEntities
        fields = ['id', 'note', 'entity_type', 'entity_value']
        read_only_fields = ['id']

class UserInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = ['id', 'user', 'note', 'interaction_type', 'timestamp']
        read_only_fields = ['id', 'timestamp']

class NoteHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteHistory
        fields = ['id', 'note', 'edited_by', 'previous_content', 'updated_content', 'change_reason', 'edited_at']
        read_only_fields = ['id', 'edited_at']
