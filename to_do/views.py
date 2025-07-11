from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import ProtectedError
from .models import (
    User, LoginHistory, Address, Contact, Note, Category, Subject, File, 
    Sharing, Notification, NotificationType, Review,
    NoteAnalysis, NoteSuggestions, ChatInteraction, NoteRecommendation, SearchLog,
    NoteTags, NoteEntities, UserInteraction, NoteHistory
)
from .serializers import (
    UserSerializer, LoginHistorySerializer, AddressSerializer, ContactSerializer,
    NoteSerializer, CategorySerializer, SubjectSerializer, FileSerializer,
    SharingSerializer, NotificationSerializer, NotificationTypeSerializer, ReviewSerializer,
    NoteAnalysisSerializer, NoteSuggestionsSerializer, ChatInteractionSerializer, 
    NoteRecommendationSerializer, SearchLogSerializer, NoteTagsSerializer, 
    NoteEntitiesSerializer, UserInteractionSerializer, NoteHistorySerializer
)

# Centralização do tratamento de exceções
def handle_exception(exception):
    if isinstance(exception, ValidationError):
        return Response(exception.detail, status=status.HTTP_400_BAD_REQUEST)
    if isinstance(exception, IntegrityError):
        return Response({'error': 'Erro de integridade do banco de dados'}, status=status.HTTP_400_BAD_REQUEST)
    if isinstance(exception, ProtectedError):
        return Response({'error': 'Não é possível excluir o objeto pois possui referências em outras entidades'},
                         status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Erro interno do servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return handle_exception(e)

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return handle_exception(e)

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            return handle_exception(e)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return handle_exception(e)

    def partial_update(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, **kwargs)
        except Exception as e:
            return handle_exception(e)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return handle_exception(e)

class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ['username', 'email']

class LoginHistoryViewSet(BaseViewSet):
    queryset = LoginHistory.objects.all()
    serializer_class = LoginHistorySerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.queryset.filter(user=self.request.user)
        return self.queryset

class AddressViewSet(BaseViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class ContactViewSet(BaseViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class NoteViewSet(BaseViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    search_fields = ['title', 'content']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubjectViewSet(BaseViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class FileViewSet(BaseViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get_queryset(self):
        return self.queryset.filter(note__user=self.request.user)

class SharingViewSet(BaseViewSet):
    queryset = Sharing.objects.all()
    serializer_class = SharingSerializer

    def get_queryset(self):
        return self.queryset.filter(shared_with=self.request.user)

class NotificationViewSet(BaseViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        try:
            unread_notifications = self.get_queryset().filter(read=False)
            serializer = self.get_serializer(unread_notifications, many=True)
            return Response(serializer.data)
        except Exception as e:
            return handle_exception(e)

class NotificationTypeViewSet(BaseViewSet):
    queryset = NotificationType.objects.all()
    serializer_class = NotificationTypeSerializer

class ReviewViewSet(BaseViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return self.queryset.filter(note__user=self.request.user)

# Novas Views para IA e funcionalidades
class NoteAnalysisViewSet(BaseViewSet):
    queryset = NoteAnalysis.objects.all()
    serializer_class = NoteAnalysisSerializer

    def get_queryset(self):
        return self.queryset.filter(note__user=self.request.user)

class NoteSuggestionsViewSet(BaseViewSet):
    queryset = NoteSuggestions.objects.all()
    serializer_class = NoteSuggestionsSerializer

    def get_queryset(self):
        return self.queryset.filter(note__user=self.request.user)

class ChatInteractionViewSet(BaseViewSet):
    queryset = ChatInteraction.objects.all()
    serializer_class = ChatInteractionSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class NoteRecommendationViewSet(BaseViewSet):
    queryset = NoteRecommendation.objects.all()
    serializer_class = NoteRecommendationSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class SearchLogViewSet(BaseViewSet):
    queryset = SearchLog.objects.all()
    serializer_class = SearchLogSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class NoteTagsViewSet(BaseViewSet):
    queryset = NoteTags.objects.all()
    serializer_class = NoteTagsSerializer

    def get_queryset(self):
        return self.queryset.filter(note__user=self.request.user)

class NoteEntitiesViewSet(BaseViewSet):
    queryset = NoteEntities.objects.all()
    serializer_class = NoteEntitiesSerializer

    def get_queryset(self):
        return self.queryset.filter(note__user=self.request.user)

class UserInteractionViewSet(BaseViewSet):
    queryset = UserInteraction.objects.all()
    serializer_class = UserInteractionSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class NoteHistoryViewSet(BaseViewSet):
    queryset = NoteHistory.objects.all()
    serializer_class = NoteHistorySerializer

    def get_queryset(self):
        return self.queryset.filter(note__user=self.request.user)
