from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('to_do.urls')),  # Substitua 'your_app_name' pelo nome do seu app
]
