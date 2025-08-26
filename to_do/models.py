from django.db import models
from django.contrib.auth.models import (
    AbstractUser, Group, Permission, BaseUserManager
)
from django.core.validators import (
    RegexValidator, MinValueValidator, MaxValueValidator
)
from django.utils.translation import gettext_lazy as _

# ---------------- Constants & Validators ----------------
STATE_CHOICES = (
    ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
    ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
    ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
)

PHONE_REGEX = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Formato: '+999999999'. Máx 15 dígitos."
)

POSTAL_CODE_REGEX = RegexValidator(
    regex=r'^\d{5}-?\d{3}$',
    message='CEP inválido. Formato: 00000-000'
)

RATING_CHOICES = [
    (1, 'Péssimo'), (2, 'Ruim'), (3, 'Regular'),
    (4, 'Bom'), (5, 'Excelente')
]

SENTIMENT_CHOICES = [
    ('positive', 'Positivo'),
    ('negative', 'Negativo'),
    ('neutral', 'Neutro')
]

# ---------------- User Manager ----------------
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError(_('Username é obrigatório'))
        if not email:
            raise ValueError(_('Email é obrigatório'))

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_('Superuser deve ter is_staff=True.'))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_('Superuser deve ter is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)

# ---------------- User Model ----------------
class User(AbstractUser):
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Data de Nascimento")
    )
    email = models.EmailField(
        unique=True,
        db_index=True,
        verbose_name=_("Email")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Data de Criação")
    )
    groups = models.ManyToManyField(
        Group,
        related_name='custom_users',
        blank=True,
        verbose_name=_('groups'),
        help_text=_('Grupos aos quais este usuário pertence.')
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users',
        blank=True,
        verbose_name=_('user permissions'),
        help_text=_('Permissões específicas para este usuário.')
    )

    objects = UserManager()

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email'], name='email_idx'),
        ]

    def __str__(self):
        return self.username

# ---------------- Login History ----------------
class LoginHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='login_histories'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(
        verbose_name=_("Endereço IP")
    )
    user_agent = models.CharField(
        max_length=255,
        verbose_name=_("User Agent")
    )

    class Meta:
        verbose_name = _("Histórico de Login")
        verbose_name_plural = _("Históricos de Login")
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
        ]

# ---------------- Address ----------------
class Address(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    state = models.CharField(
        max_length=2,
        choices=STATE_CHOICES,
        verbose_name=_("Estado")
    )
    street = models.CharField(
        max_length=100,
        verbose_name=_("Rua")
    )
    number = models.CharField(
        max_length=20,
        verbose_name=_("Número")
    )
    complement = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Complemento")
    )
    neighborhood = models.CharField(
        max_length=100,
        verbose_name=_("Bairro")
    )
    city = models.CharField(
        max_length=100,
        verbose_name=_("Cidade")
    )
    postal_code = models.CharField(
        max_length=9,
        validators=[POSTAL_CODE_REGEX],
        verbose_name=_("CEP")
    )

    class Meta:
        verbose_name = _("Endereço")
        verbose_name_plural = _("Endereços")
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'postal_code'],
                name='unique_user_address'
            )
        ]

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}/{self.state}"

# ---------------- Contact ----------------
class Contact(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='contacts'
    )
    landline = models.CharField(
        max_length=20,
        blank=True,
        validators=[PHONE_REGEX],
        verbose_name=_("Telefone Fixo")
    )
    mobile_phone = models.CharField(
        max_length=20,
        validators=[PHONE_REGEX],
        verbose_name=_("Celular")
    )

    class Meta:
        verbose_name = _("Contato")
        verbose_name_plural = _("Contatos")

# ---------------- Category & Subject ----------------
class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Nome")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Descrição")
    )

    class Meta:
        verbose_name = _("Categoria")
        verbose_name_plural = _("Categorias")
        ordering = ['name']

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Nome")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Descrição")
    )

    class Meta:
        verbose_name = _("Assunto")
        verbose_name_plural = _("Assuntos")
        ordering = ['name']

    def __str__(self):
        return self.name

# ---------------- Note ----------------
class Note(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_("Título"),
        db_index=True
    )
    content = models.TextField(
        verbose_name=_("Conteúdo")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Criado em")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Atualizado em")
    )
    completed = models.BooleanField(
        default=False,
        verbose_name=_("Completo?")
    )
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='notes',
        verbose_name=_("Categorias")
    )
    subjects = models.ManyToManyField(
        Subject,
        blank=True,
        related_name='notes',
        verbose_name=_("Assuntos")
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'title'],
                name='unique_user_note_title'
            )
        ]
        verbose_name = _("Nota")
        verbose_name_plural = _("Notas")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def __str__(self):
        return self.title

# ---------------- File ----------------
class File(models.Model):
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='files'
    )
    file = models.FileField(
        upload_to='notes/files/%Y/%m/%d/',
        verbose_name=_("Arquivo")
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Enviado em")
    )

    class Meta:
        verbose_name = _("Arquivo")
        verbose_name_plural = _("Arquivos")
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.file.name

# ---------------- Sharing ----------------
class Sharing(models.Model):
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='shares'
    )
    shared_with = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shared_notes'
    )
    shared_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Compartilhado em")
    )
    can_edit = models.BooleanField(
        default=False,
        verbose_name=_("Pode editar?")
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['note', 'shared_with'],
                name='unique_note_sharing'
            )
        ]
        verbose_name = _("Compartilhamento")
        verbose_name_plural = _("Compartilhamentos")
        ordering = ['-shared_at']

# ---------------- Notification ----------------
class NotificationType(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Tipo de Notificação")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Descrição")
    )
    template = models.TextField(
        verbose_name=_("Modelo de Mensagem")
    )

    class Meta:
        verbose_name = _("Tipo de Notificação")
        verbose_name_plural = _("Tipos de Notificação")

    def __str__(self):
        return self.name

class Notification(models.Model):
    type = models.ForeignKey(
        NotificationType,
        on_delete=models.PROTECT,
        related_name='notifications'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    message = models.TextField(
        verbose_name=_("Mensagem")
    )
    sent_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Enviada em")
    )
    read = models.BooleanField(
        default=False,
        verbose_name=_("Lida?")
    )

    class Meta:
        verbose_name = _("Notificação")
        verbose_name_plural = _("Notificações")
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['sent_at']),
        ]

# ---------------- Review ----------------
class Review(models.Model):
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_("Comentário")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Criado em")
    )

    class Meta:
        verbose_name = _("Avaliação")
        verbose_name_plural = _("Avaliações")
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['note', 'reviewer'],
                name='unique_note_reviewer'
            )
        ]

# ---------------- AI Models ----------------
class NoteAnalysis(models.Model):
    note = models.OneToOneField(
        Note,
        on_delete=models.CASCADE,
        related_name='analysis'
    )
    summary = models.TextField(
        verbose_name=_("Resumo")
    )
    sentiment = models.CharField(
        max_length=20,
        choices=SENTIMENT_CHOICES,
        verbose_name=_("Sentimento")
    )
    keywords = models.JSONField(
        default=list,
        verbose_name=_("Palavras-chave")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Criado em")
    )

    class Meta:
        verbose_name = _("Análise de Nota")
        verbose_name_plural = _("Análises de Notas")
        ordering = ['-created_at']

class NoteSuggestion(models.Model):
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='suggestions'
    )
    suggestion = models.TextField(
        verbose_name=_("Sugestão")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Criado em")
    )
    applied = models.BooleanField(
        default=False,
        verbose_name=_("Aplicada?")
    )

    class Meta:
        verbose_name = _("Sugestão de Nota")
        verbose_name_plural = _("Sugestões de Notas")
        ordering = ['-created_at']

class ChatInteraction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_interactions'
    )
    message = models.TextField(
        verbose_name=_("Mensagem")
    )
    response = models.TextField(
        verbose_name=_("Resposta")
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Data/Hora")
    )
    note_context = models.ForeignKey(
        Note,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _("Interação de Chat")
        verbose_name_plural = _("Interações de Chat")
        ordering = ['-timestamp']

class NoteRecommendation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recommendations'
    )
    recommended_note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='recommended_to'
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name=_("Score")
    )
    algorithm_version = models.CharField(
        max_length=50,
        verbose_name=_("Versão do Algoritmo")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Criado em")
    )

    class Meta:
        verbose_name = _("Recomendação de Nota")
        verbose_name_plural = _("Recomendações de Notas")
        ordering = ['-score', '-created_at']
        indexes = [
            models.Index(fields=['user', '-score']),
        ]

# ---------------- Logs & Tracking ----------------
class SearchLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    query = models.CharField(
        max_length=255,
        verbose_name=_("Consulta")
    )
    results_count = models.PositiveIntegerField(
        verbose_name=_("Resultados Encontrados")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Criado em")
    )

    class Meta:
        verbose_name = _("Log de Busca")
        verbose_name_plural = _("Logs de Busca")
        ordering = ['-created_at']

class NoteTag(models.Model):
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='tags'
    )
    tag = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name=_("Tag")
    )

    class Meta:
        verbose_name = _("Tag de Nota")
        verbose_name_plural = _("Tags de Notas")
        constraints = [
            models.UniqueConstraint(
                fields=['note', 'tag'],
                name='unique_note_tag'
            )
        ]

class NoteEntity(models.Model):
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='entities'
    )
    entity_type = models.CharField(
        max_length=100,
        verbose_name=_("Tipo de Entidade")
    )
    entity_value = models.CharField(
        max_length=255,
        verbose_name=_("Valor da Entidade")
    )

    class Meta:
        verbose_name = _("Entidade de Nota")
        verbose_name_plural = _("Entidades de Notas")
        indexes = [
            models.Index(fields=['entity_type']),
        ]

class UserInteraction(models.Model):
    INTERACTION_CHOICES = [
        ('view', 'Visualização'),
        ('edit', 'Edição'),
        ('share', 'Compartilhamento'),
        ('rate', 'Avaliação'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='interactions'
    )
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='interactions'
    )
    interaction_type = models.CharField(
        max_length=20,
        choices=INTERACTION_CHOICES,
        verbose_name=_("Tipo de Interação")
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Data/Hora")
    )
    metadata = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_("Metadados")
    )

    class Meta:
        verbose_name = _("Interação do Usuário")
        verbose_name_plural = _("Interações dos Usuários")
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['interaction_type']),
        ]

class NoteHistory(models.Model):
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='history'
    )
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='note_edits'
    )
    previous_content = models.TextField(
        verbose_name=_("Conteúdo Anterior")
    )
    edited_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Editado em")
    )

    class Meta:
        verbose_name = _("Histórico de Nota")
        verbose_name_plural = _("Históricos de Notas")
        ordering = ['-edited_at']
