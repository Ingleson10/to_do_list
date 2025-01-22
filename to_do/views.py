from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    User, LoginHistory, Address, Contact, Note, Category, Subject, File, 
    Sharing, Notification, NotificationType, Review
)
from .serializers import (
    UserSerializer, LoginHistorySerializer, AddressSerializer, ContactSerializer,
    NoteSerializer, CategorySerializer, SubjectSerializer, FileSerializer,
    SharingSerializer, NotificationSerializer, NotificationTypeSerializer, ReviewSerializer
)

# Define a classe base com permissões padrão
class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]  # Requer autenticação para acessar as views
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]  # Filtros globais

class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ['username', 'email']  # Permite buscas por username ou email

class LoginHistoryViewSet(BaseViewSet):
    queryset = LoginHistory.objects.all()
    serializer_class = LoginHistorySerializer

    def get_queryset(self):
        # Retorna apenas o histórico do usuário autenticado
        if not self.request.user.is_staff:
            return self.queryset.filter(user=self.request.user)
        return self.queryset

class AddressViewSet(BaseViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        # Filtro por usuário
        return self.queryset.filter(user=self.request.user)

class ContactViewSet(BaseViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_queryset(self):
        # Filtro por usuário
        return self.queryset.filter(user=self.request.user)

class NoteViewSet(BaseViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    search_fields = ['title', 'content']  # Permite buscar por título ou conteúdo

    def get_queryset(self):
        # Retorna apenas notas do usuário autenticado
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
        # Retorna apenas arquivos vinculados a notas do usuário
        return self.queryset.filter(note__user=self.request.user)

class SharingViewSet(BaseViewSet):
    queryset = Sharing.objects.all()
    serializer_class = SharingSerializer

    def get_queryset(self):
        # Filtro por notas compartilhadas com o usuário
        return self.queryset.filter(shared_with=self.request.user)

class NotificationViewSet(BaseViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Filtro por notificações do usuário autenticado
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        # Endpoint para notificações não lidas
        unread_notifications = self.get_queryset().filter(read=False)
        serializer = self.get_serializer(unread_notifications, many=True)
        return Response(serializer.data)

class NotificationTypeViewSet(BaseViewSet):
    queryset = NotificationType.objects.all()
    serializer_class = NotificationTypeSerializer

class ReviewViewSet(BaseViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # Filtro por notas do usuário autenticado
        return self.queryset.filter(note__user=self.request.user)
