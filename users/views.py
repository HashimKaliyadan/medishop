# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.urls import reverse
from .forms import UserRegistrationForm, EmailAuthenticationForm

def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # saves as customer by default
            messages.success(request, "Account created. Please log in.")
            return redirect("users:login")
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})


from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            # 🔑 ROLE-BASED REDIRECT
            if getattr(user, "is_manager", False):
                return redirect("managers:dashboard")
            else:
                return redirect("customers:home")

    return render(request, "users/login.html")



def logout_view(request):
    logout(request)
    return redirect("customers:home")
