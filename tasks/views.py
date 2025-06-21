from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Welcome to the Task Management System")

def contact(request):
    return HttpResponse("<h1 style= 'color: red'>This is the contact page</h1>")

def show_task(request):
    return HttpResponse("This is the show task page")