from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hell/', include('myapp.urls')),
    path('calc/', include('calculator.urls')),
]