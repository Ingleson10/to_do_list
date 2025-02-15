from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    UserViewSet, LoginHistoryViewSet, AddressViewSet, ContactViewSet, NoteViewSet,
    CategoryViewSet, SubjectViewSet, FileViewSet, SharingViewSet, NotificationViewSet,
    NotificationTypeViewSet, ReviewViewSet, NoteAnalysisViewSet, NoteSuggestionsViewSet,
    ChatInteractionViewSet, NoteRecommendationViewSet, SearchLogViewSet, NoteTagsViewSet,
    NoteEntitiesViewSet, UserInteractionViewSet, NoteHistoryViewSet
)

# Configuração do roteador padrão
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'login-histories', LoginHistoryViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'files', FileViewSet)
router.register(r'sharings', SharingViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'notification-types', NotificationTypeViewSet)
router.register(r'reviews', ReviewViewSet)

# Novos endpoints para IA e funcionalidades relacionadas
router.register(r'note-analyses', NoteAnalysisViewSet)
router.register(r'note-suggestions', NoteSuggestionsViewSet)
router.register(r'chat-interactions', ChatInteractionViewSet)
router.register(r'note-recommendations', NoteRecommendationViewSet)
router.register(r'search-logs', SearchLogViewSet)
router.register(r'note-tags', NoteTagsViewSet)
router.register(r'note-entities', NoteEntitiesViewSet)
router.register(r'user-interactions', UserInteractionViewSet)
router.register(r'note-history', NoteHistoryViewSet)

# Configuração de URLs
urlpatterns = [
    # Endpoints da API REST registrados no roteador
    path('', include(router.urls)),

    # Endpoints de autenticação com JWT
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Endpoints adicionais para autenticação (opcional)
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),  # Navegador API Login/Logout
]
