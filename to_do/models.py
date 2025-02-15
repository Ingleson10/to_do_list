from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    email = models.EmailField(unique=True, verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255, verbose_name="User Agent")

class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
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
    postal_code = models.CharField(max_length=9)

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    landline = models.CharField(max_length=20, blank=True)
    mobile_phone = models.CharField(max_length=20)

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Title")
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

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

class File(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    file = models.FileField(upload_to='notes/files')

class Sharing(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_notes')

class Notification(models.Model):
    type = models.ForeignKey('NotificationType', on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class NotificationType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Notification Type")
    description = models.TextField(blank=True)

class Review(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')])
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


# ------------------ Novas Tabelas e Funcionalidades de IA ------------------

# Tabela para armazenar as análises automáticas de notas (resumos, sentimentos)
class NoteAnalysis(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    summary = models.TextField()  # Resumo gerado pela IA
    sentiment = models.CharField(max_length=20)  # Sentimento detectado (ex: "positivo", "negativo")
    created_at = models.DateTimeField(auto_now_add=True)

# Tabela para armazenar sugestões automáticas de melhorias nas notas
class NoteSuggestions(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    suggestion = models.TextField()  # Sugestão gerada pela IA
    created_at = models.DateTimeField(auto_now_add=True)

# Tabela para armazenar as interações com o chatbot
class ChatInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()  # Mensagem enviada pelo usuário
    response = models.TextField()  # Resposta do chatbot
    timestamp = models.DateTimeField(auto_now_add=True)

# Tabela para armazenar recomendações de notas feitas pela IA para o usuário
class NoteRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommended_note = models.ForeignKey(Note, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)  # Relevância da recomendação
    created_at = models.DateTimeField(auto_now_add=True)

# Tabela para armazenar logs de pesquisa semântica
class SearchLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()  # Consulta de pesquisa feita pelo usuário
    search_results = models.JSONField()  # IDs das notas encontradas
    created_at = models.DateTimeField(auto_now_add=True)

# Tabela para armazenar as tags geradas automaticamente para as notas
class NoteTags(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=100)  # Nome da tag gerada pela IA

# Tabela para armazenar entidades extraídas das notas (ex: nomes, locais, datas)
class NoteEntities(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    entity_type = models.CharField(max_length=100)  # Tipo da entidade (ex: "pessoa", "local")
    entity_value = models.CharField(max_length=255)  # Valor da entidade extraída

# Tabela para registrar o comportamento de interação do usuário com notas
class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50)  # Tipo de interação (ex: "visualização", "comentário")
    timestamp = models.DateTimeField(auto_now_add=True)

# Tabela para armazenar o histórico de edições nas notas
class NoteHistory(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    previous_content = models.TextField()  # Conteúdo anterior da nota
    updated_content = models.TextField()  # Novo conteúdo da nota
    change_reason = models.TextField()  # Razão da alteração (gerada pela IA)
    edited_at = models.DateTimeField(auto_now_add=True)
