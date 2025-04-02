# musicdepot/urls.py

from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect  # Required for root redirect
from .views import client_list, instructor_list

urlpatterns = [
    path('', lambda request: redirect('/admin/', permanent=False)),  # Root -> /admin/
    path('admin/', admin.site.urls),
    path('clients/', client_list, name='client-list'),
    path('instructors/', instructor_list, name='instructor-list'),
]
