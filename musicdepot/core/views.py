from django.shortcuts import render
from .models import Client, Instructor

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'core/client_list.html', {'clients': clients})

def instructor_list(request):
    instructors = Instructor.objects.all()
    return render(request, 'core/instructor_list.html', {'instructors': instructors})
