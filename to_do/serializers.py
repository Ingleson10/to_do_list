from rest_framework import serializers
from .models import User, LoginHistory, Address, Contact, Note, Category, Subject, File, Sharing, Notification, NotificationType, Review  # Importando os modelos

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = ['id', 'user', 'timestamp', 'ip_address']  # Removido 'state' que não está no modelo
        read_only_fields = ['id', 'timestamp']

    def validate_ip_address(self, value):
        return value
    
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'state', 'street', 'number', 'complement', 'neighborhood', 'city', 'postal_code']
        read_only_fields = ['id']  # O ID deve ser somente leitura

    def validate_postal_code(self, value):
        # Validação opcional para o código postal
        return value
    
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'user', 'landline', 'mobile_phone']
        read_only_fields = ['id']  # O ID deve ser somente leitura

    def validate_mobile_phone(self, value):
        # Validação opcional para o telefone móvel
        return value
    
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at', 'completed']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']  # Campos que não devem ser alterados pelo usuário

    def validate_title(self, value):
        # Validação opcional para garantir que o título não esteja vazio
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value
    
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
