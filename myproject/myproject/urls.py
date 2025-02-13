from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', include('myapp.urls')),
    path('calculator/', include('calculator.urls')),
]