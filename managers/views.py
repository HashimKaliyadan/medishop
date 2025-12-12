from django.shortcuts import render
from main.decorators import allow_manager

@allow_manager
def manager_home(request):
    return render(request, "managers/home.html")