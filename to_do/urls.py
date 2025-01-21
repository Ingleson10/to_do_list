from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    LoginHistoryViewSet,
    AddressViewSet,
    ContactViewSet,
    NoteViewSet,
    CategoryViewSet,
    SubjectViewSet,
    FileViewSet,
    SharingViewSet,
    NotificationViewSet,
    ReviewViewSet
)

# Configurando o roteador para ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'login-history', LoginHistoryViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'files', FileViewSet)
router.register(r'sharing', SharingViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Inclui todas as rotas geradas automaticamente pelo router
]