from rest_framework import viewsets
from .models import User, LoginHistory, Address, Contact, Note, Category, Subject, File, Sharing, Notification, Review
from .serializers import UserSerializer, LoginHistorySerializer, AddressSerializer, ContactSerializer, NoteSerializer, CategorySerializer, SubjectSerializer, FileSerializer, SharingSerializer, NotificationSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginHistoryViewSet(viewsets.ModelViewSet):
    queryset = LoginHistory.objects.all()
    serializer_class = LoginHistorySerializer
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

    def perform_create(self, serializer):
        # Aqui você pode adicionar lógica adicional ao criar um registro de login, se necessário
        serializer.save(user=self.request.user)  # Atribui automaticamente o usuário logado ao histórico de login

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Atribui automaticamente o usuário logado ao endereço
        serializer.save(user=self.request.user)

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Atribui automaticamente o usuário logado ao contato
        serializer.save(user=self.request.user)

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Atribui automaticamente o usuário logado à nota
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Filtra as notas para retornar apenas as do usuário autenticado
        return self.queryset.filter(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

class SharingViewSet(viewsets.ModelViewSet):
    queryset = Sharing.objects.all()
    serializer_class = SharingSerializer
    permission_classes = [IsAuthenticated]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]