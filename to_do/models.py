from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.core.validators import RegexValidator

# ---------------- User Manager ----------------
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('O username é obrigatório')
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

# ---------------- User Model ----------------
class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    email = models.EmailField(unique=True, verbose_name="Email", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')
    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']

    def __str__(self):
        return self.username

# ---------------- Login History ----------------
class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(verbose_name="User Agent")

    class Meta:
        verbose_name = "Login History"
        verbose_name_plural = "Login Histories"
        ordering = ['-timestamp']

# ---------------- Address ----------------
class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=2, choices=[
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ], verbose_name="State")
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    complement = models.CharField(max_length=100, blank=True)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=9, validators=[
        RegexValidator(r'^\d{5}-?\d{3}$', 'Digite um CEP válido no formato 00000-000')
    ])

# ---------------- Contact ----------------
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    landline = models.CharField(max_length=20, blank=True)
    mobile_phone = models.CharField(max_length=20)

# ---------------- Note ----------------
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Title", db_index=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    categories = models.ManyToManyField('Category', blank=True, related_name='notes')
    subjects = models.ManyToManyField('Subject', blank=True, related_name='notes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'title'], name='unique_user_note_title')
        ]
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

# ---------------- Category & Subject ----------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# ---------------- File ----------------
class File(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    file = models.FileField(upload_to='notes/files')

# ---------------- Sharing ----------------
class Sharing(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_notes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['note', 'shared_with'], name='unique_note_sharing')
        ]

# ---------------- Notification ----------------
class NotificationType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Notification Type")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Notification(models.Model):
    type = models.ForeignKey('NotificationType', on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# ---------------- Review ----------------
class Review(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[
        (1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')
    ])
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

# ---------------- IA: Analysis, Suggestion, Chat, Recommendation ----------------
class NoteAnalysis(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral')
    ]
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    summary = models.TextField()
    sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

class NoteSuggestions(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    suggestion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ChatInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# ---------------- IA: Logs, Tags, Entidades, Histórico ----------------
class NoteRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommended_note = models.ForeignKey(Note, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class SearchLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()
    search_results = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class NoteTags(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=100)

class NoteEntities(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    entity_type = models.CharField(max_length=100)
    entity_value = models.CharField(max_length=255)

class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

class NoteHistory(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    previous_content = models.TextField()
    updated_content = models.TextField()
    change_reason = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-edited_at']
        verbose_name = "Review"
        verbose_name_plural = "Reviews"