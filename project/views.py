from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'project/index.html', {})

def create_project(request):
    return render(request, 'project/addproject.html',{})