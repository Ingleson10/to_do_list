from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('to_do.urls')),
    path('auth/', include('rest_framework.urls')),
    #path('auth/token/', include('to_do.urls')),
    #path('', include('rest_framework.urls')),
]
