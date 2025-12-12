from django.shortcuts import render
from main.decorators import allow_customer

def customer_home(request):
    return render(request, "customers/home.html")

@allow_customer
def account(request):
    return render(request, "customers/account.html")