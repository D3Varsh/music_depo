from django.urls import path
from .views import client_list, instructor_list

urlpatterns = [
    path('clients/', client_list, name='client-list'),
    path('instructors/', instructor_list, name='instructor-list'),
]
