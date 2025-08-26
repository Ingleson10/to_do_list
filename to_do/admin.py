from django.contrib import admin
from .models import (
    User, LoginHistory, Address, Contact, Note, Category, Subject, File, 
    Sharing, Notification, NotificationType, Review,
    NoteAnalysis, NoteSuggestion, ChatInteraction, NoteRecommendation, 
    SearchLog, NoteTag, NoteEntity, UserInteraction, NoteHistory
)

# Personalização de Admin para User
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_of_birth', 'created_at', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')

# Personalização de Admin para Note
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at', 'completed')
    search_fields = ('title', 'user__username')
    list_filter = ('completed', 'created_at')

# Registrando modelos no Admin
admin.site.register(User, UserAdmin)
admin.site.register(LoginHistory)
admin.site.register(Address)
admin.site.register(Contact)
admin.site.register(Note, NoteAdmin)
admin.site.register(Category)
admin.site.register(Subject)
admin.site.register(File)
admin.site.register(Sharing)
admin.site.register(Notification)
admin.site.register(NotificationType)
admin.site.register(Review)
admin.site.register(NoteAnalysis)
admin.site.register(NoteSuggestion) 
admin.site.register(ChatInteraction)
admin.site.register(NoteRecommendation)
admin.site.register(SearchLog)
admin.site.register(NoteTag)       
admin.site.register(NoteEntity)      
admin.site.register(UserInteraction)
admin.site.register(NoteHistory)
