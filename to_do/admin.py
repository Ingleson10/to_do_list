from django.contrib import admin
from .models import User, LoginHistory, Address, Contact, Note, Category, Subject, File, Sharing, Notification, NotificationType, Review

admin.site.register(User)
admin.site.register(LoginHistory)
admin.site.register(Address)
admin.site.register(Contact)
admin.site.register(Note)
admin.site.register(Category)
admin.site.register(Subject)
admin.site.register(File)
admin.site.register(Sharing)
admin.site.register(Notification)
admin.site.register(NotificationType)
admin.site.register(Review)
